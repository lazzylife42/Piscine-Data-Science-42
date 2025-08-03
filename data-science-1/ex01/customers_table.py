from sqlalchemy import create_engine, text

# Database configuration
DATABASE_CONFIG = {
	'host': 'localhost',
	'port': '5432',
	'database': 'piscineds',
	'username': 'smonte',
	'password': 'mysecretpassword'
}

DATABASE_URL = f"postgresql://{DATABASE_CONFIG['username']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}?gssencmode=disable"

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
	# Find all tables matching pattern data_202%
	result = conn.execute(text("""
		SELECT table_name 
		FROM information_schema.tables 
		WHERE table_schema = 'public' 
		AND table_name LIKE 'data_202%'
		ORDER BY table_name
	"""))
	
	tables = [row[0] for row in result]
	
	if not tables:
		print("No tables found matching pattern data_202%")
		exit()
	
	# Drop customers table if exists
	conn.execute(text("DROP TABLE IF EXISTS customers"))
	conn.commit()
	
	# Create UNION ALL query
	union_query = " UNION ALL ".join([f"SELECT * FROM {table}" for table in tables])
	create_query = f"CREATE TABLE customers AS {union_query}"
	
	# Execute create table
	conn.execute(text(create_query))
	conn.commit()
	
	# Count records
	result = conn.execute(text("SELECT COUNT(*) FROM customers"))
	count = result.scalar()
	
	print(f"Created customers table from {len(tables)} tables with {count} records")
	