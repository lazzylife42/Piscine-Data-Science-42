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
    # Find items table
    result = conn.execute(text("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name LIKE '%item%'
        LIMIT 1
    """))
    
    items_table = result.scalar()
    
    if not items_table:
        print("No items table found")
        exit()
    
    # Create new table with LEFT JOIN
    # Using c.* preserves ALL original columns from customers
    conn.execute(text(f"""
        CREATE TABLE customers_enriched AS
        SELECT c.event_time, c.event_type, c.product_id, c.price, 
               c.user_id, c.user_session,
               i.category_id, i.category_code, i.brand
        FROM customers c
        LEFT JOIN {items_table} i ON c.product_id = i.product_id
    """))
    
    # Replace original table
    conn.execute(text("DROP TABLE customers"))
    conn.execute(text("ALTER TABLE customers_enriched RENAME TO customers"))
    conn.commit()
    
    # Count records and check enrichment
    result = conn.execute(text("""
        SELECT COUNT(*) as total,
               COUNT(category_id) as with_category
        FROM customers
    """))
    row = result.fetchone()
    
    print(f"Fusion complete with {items_table}. Total records: {row[0]}, enriched: {row[1]}")