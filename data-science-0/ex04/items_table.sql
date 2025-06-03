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