-- "docker exec -it postgres_local psql -U smonte -d piscineds -W -h localhost -f workspace/ex02/table.sql"

-- Table pour data_2022_oct
DROP TABLE IF EXISTS data_2022_oct;

CREATE TABLE data_2022_oct (
event_time TIMESTAMP,           
event_type VARCHAR(50),         
product_id BIGINT,              
price DECIMAL(10,2),            
user_id BIGINT,                  
user_session UUID  
);

-- Table pour data_2022_nov
DROP TABLE IF EXISTS data_2022_nov;

CREATE TABLE data_2022_nov (
    event_time TIMESTAMP,
    event_type VARCHAR(50),
    product_id BIGINT,
    price DECIMAL(10,2),
    user_id BIGINT,
    user_session UUID
);

-- Table pour data_2022_dec
DROP TABLE IF EXISTS data_2022_dec;

CREATE TABLE data_2022_dec (
    event_time TIMESTAMP,
    event_type VARCHAR(50),
    product_id BIGINT,
    price DECIMAL(10,2),
    user_id BIGINT,
    user_session UUID
);

-- Table pour data_2023_jan
DROP TABLE IF EXISTS data_2023_jan;

CREATE TABLE data_2023_jan (
    event_time TIMESTAMP,
    event_type VARCHAR(50),
    product_id BIGINT,
    price DECIMAL(10,2),
    user_id BIGINT,
    user_session UUID
);

-- Import data from CSV files

COPY data_2022_oct FROM '/workspace/subject/customer/data_2022_oct.csv' 
WITH (FORMAT CSV, HEADER true, DELIMITER ',');

COPY data_2022_nov FROM '/workspace/subject/customer/data_2022_nov.csv' 
WITH (FORMAT CSV, HEADER true, DELIMITER ',');

COPY data_2022_dec FROM '/workspace/subject/customer/data_2022_dec.csv' 
WITH (FORMAT CSV, HEADER true, DELIMITER ',');

COPY data_2023_jan FROM '/workspace/subject/customer/data_2023_jan.csv' 
WITH (FORMAT CSV, HEADER true, DELIMITER ',');
