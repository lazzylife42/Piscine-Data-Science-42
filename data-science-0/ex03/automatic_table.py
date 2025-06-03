import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import subprocess
import time

# Database configuration
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'database': 'piscineds',
    'username': 'smonte',
    'password': 'mysecretpassword'
}

DATABASE_URL = f"postgresql://{DATABASE_CONFIG['username']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}?gssencmode=disable"

class AutomaticTable:
    def __init__(self):
        self.engine = None
        # Check both customer and item folders
        self.base_folder = Path("../subject")
        self.csv_folders = [
            self.base_folder / "customer",
            self.base_folder / "item"
        ]
        
    def connect(self):
        """Establish database connection"""
        try:
            self.engine = create_engine(DATABASE_URL, echo=False)
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                print("Database connection successful")
                return True
        except SQLAlchemyError as e:
            raise ConnectionError(f"Database connection failed: {e}")
    
    def get_csv_files(self):
        """List all CSV files in both customer and item folders"""
        all_csv_files = []
        
        for folder in self.csv_folders:
            if folder.exists():
                csv_files = list(folder.glob("*.csv"))
                all_csv_files.extend(csv_files)
                print(f"CSV files in {folder.name}: {[f.name for f in csv_files]}")
            else:
                print(f"Folder {folder} does not exist")
        
        if not all_csv_files:
            raise FileNotFoundError("No CSV files found in any folder")
            
        return all_csv_files
    
    def extract_table_name(self, csv_filename):
        """Extract table name from CSV filename"""
        name = csv_filename.stem
        table_name = name.replace("-", "_").replace(" ", "_").lower()
        return table_name
    
    def get_table_type(self, csv_file):
        """Determine table type based on file location"""
        if "item" in str(csv_file.parent):
            return "item"
        else:
            return "data"
    
    def create_table_for_item_files(self, table_name):
        """Create table for item files"""
        create_table_sql = f"""
        DROP TABLE IF EXISTS {table_name};
        CREATE TABLE {table_name} (
            product_id BIGINT,
            category_id BIGINT,
            category_code VARCHAR(255),
            brand VARCHAR(255)
        );
        """
        return create_table_sql
    
    def create_table_for_data_files(self, table_name):
        """Create table for data_* files (customer events)"""
        create_table_sql = f"""
        DROP TABLE IF EXISTS {table_name};
        CREATE TABLE {table_name} (
            event_time TIMESTAMP,
            event_type VARCHAR(50),
            product_id BIGINT,
            price DECIMAL(10,2),
            user_id BIGINT,
            user_session UUID
        );
        """
        return create_table_sql
    
    def import_with_docker_copy(self, csv_file, table_name, container_name="postgres_local"):
        """Import CSV using docker exec and COPY command"""
        try:
            relative_path = csv_file.relative_to(Path("../"))
            container_path = f"/workspace/{relative_path}"
            
            # Docker exec command with psql
            cmd = [
                "docker", "exec", "-i", container_name,
                "psql", "-U", DATABASE_CONFIG['username'], "-d", DATABASE_CONFIG['database'],
                "-c", f"COPY {table_name} FROM '{container_path}' WITH (FORMAT CSV, HEADER true);"
            ]
            
            print(f"Executing: docker exec {container_name} psql -c \"COPY {table_name} FROM '{container_path}'...\"")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"Successfully imported {csv_file.name} into {table_name}")
                return True
            else:
                print(f"Error importing {csv_file.name}: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Error with docker exec: {e}")
            return False
    
    def create_tables_and_import(self, container_name="postgres_local"):
        """Create tables and import data using docker exec"""
        if not self.engine:
            self.connect()
        
        csv_files = self.get_csv_files()
        if not csv_files:
            print("No CSV files found")
            return
        
        created_tables = []
        
        try:
            # Create tables first
            with self.engine.connect() as conn:
                for csv_file in csv_files:
                    table_name = self.extract_table_name(csv_file)
                    table_type = self.get_table_type(csv_file)
                    
                    print(f"Creating table: {table_name} (type: {table_type})")
                    
                    if table_type == "item":
                        create_sql = self.create_table_for_item_files(table_name)
                    else:
                        create_sql = self.create_table_for_data_files(table_name)
                    
                    conn.execute(text(create_sql))
                    print(f"Table {table_name} created")
                    created_tables.append(table_name)
                
                conn.commit()
                print(f"\n{len(created_tables)} tables created successfully")
                
            # Import data using docker exec
            print("\nImporting data using docker exec...")
            successful_imports = 0
            
            for csv_file in csv_files:
                table_name = self.extract_table_name(csv_file)
                print(f"Importing {csv_file.name} into {table_name}...")
                
                if self.import_with_docker_copy(csv_file, table_name, container_name):
                    successful_imports += 1
                
            print(f"\n{successful_imports}/{len(csv_files)} files imported successfully")
                
        except SQLAlchemyError as e:
            print(f"Error: {e}")
            raise

def main():
    creator = AutomaticTable()
    
    try:
        print("Creating tables and importing data with docker exec...")
        creator.create_tables_and_import(container_name="postgres_local")
        print("\nProcess completed successfully!")
        
    except Exception as e:
        print(f"Process failed: {e}")

if __name__ == "__main__":
    main()