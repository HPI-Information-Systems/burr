\c postgres
\set database_name normalized__redundancy__person_address
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = :'database_name' AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS :database_name;
CREATE DATABASE :database_name;
\c :database_name;
SET default_tablespace = '';
SET default_with_oids = false;

CREATE TABLE person (
    id int,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(50),
    department VARCHAR(50),
    department_id int,
    address_id int,
    street VARCHAR(50),
    house_number VARCHAR(50),
    zip VARCHAR(50),
    city VARCHAR(50),
    state VARCHAR(50)
);

CREATE TABLE cost_center (
    id int,
    name VARCHAR(50),
    department_id int,
    department VARCHAR(50)
);

ALTER TABLE Only person
    ADD CONSTRAINT person_primary_key PRIMARY KEY (id);

copy person (id, first_name, last_name, email, department, department_id,address_id, street, house_number, zip, city, state)
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,John,Doe,'john.doe@gmail.com',IT,1,1,Main Street,1,12345,New York,NY
2,Jane,Doe,'jane.doe@mail.de',HR,2,2,Second Street,2,23456,Los Angeles,CA
3,Jim,Doe,'jimdoe@mail.com',Marketing,3,3,Third Street,3,34567,Chicago,IL
4,Jack,Doe,'jackdoe@hotmail.en',HR,2,1,Main Street,1,12345,New York,NY
\.

copy cost_center (id, name, department_id, department)
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,COST-IT,1,IT
2,COST-HR,2,HR
3,COST-Marketing,3,Marketing
4,COST-IT-2,1,IT
\.
