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
    # Create new table with LEFT JOIN using DISTINCT ON to avoid duplicates
    conn.execute(text("""
        CREATE TABLE customers_enriched AS
        SELECT c.event_time, c.event_type, c.product_id, c.price, 
            c.user_id, c.user_session,
            i.category_id, i.category_code, i.brand
        FROM customers c
        LEFT JOIN (
            SELECT product_id, 
                MAX(category_id) as category_id,
                MAX(category_code) as category_code, 
                MAX(brand) as brand
            FROM item
            WHERE category_id IS NOT NULL 
            OR category_code IS NOT NULL 
            OR brand IS NOT NULL
            GROUP BY product_id
        ) i ON c.product_id = i.product_id
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
    
    print(f"Fusion complete with item. Total records: {row[0]}, enriched: {row[1]}")