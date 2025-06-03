-- "docker exec -it postgres_local psql -U smonte -d piscineds -W -h localhost -f workspace/ex04/items_table.sql"

-- Table structure for item.csv

DROP TABLE IF EXISTS item;

CREATE TABLE item (
    product_id BIGINT,
    category_id BIGINT,
    category_code VARCHAR(255),
    brand VARCHAR(255)
);

-- Import data from CSV file
COPY item FROM '/workspace/subject/item/item.csv' WITH (FORMAT CSV, HEADER true);