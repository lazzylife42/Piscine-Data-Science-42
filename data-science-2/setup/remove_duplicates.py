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
    # Count before deduplication
    result = conn.execute(text("SELECT COUNT(*) FROM customers"))
    count_before = result.scalar()
    
    # Remove exact duplicates and near-duplicates (1 second interval)
    conn.execute(text("""
        CREATE TABLE customers_temp AS
        WITH ordered_data AS (
            SELECT *,
                   LAG(event_time) OVER (PARTITION BY event_type, product_id, user_id 
                                         ORDER BY event_time) AS prev_time
            FROM customers
        )
        SELECT event_time, event_type, product_id, price, user_id, user_session
        FROM ordered_data
        WHERE prev_time IS NULL 
           OR EXTRACT(EPOCH FROM (event_time - prev_time)) > 1
        ORDER BY event_time
    """))
    
    # Replace original table
    conn.execute(text("DROP TABLE customers"))
    conn.execute(text("ALTER TABLE customers_temp RENAME TO customers"))
    conn.commit()
    
    # Count after deduplication
    result = conn.execute(text("SELECT COUNT(*) FROM customers"))
    count_after = result.scalar()
    
    print(f"Removed {count_before - count_after} duplicates. Records: {count_before} -> {count_after}")