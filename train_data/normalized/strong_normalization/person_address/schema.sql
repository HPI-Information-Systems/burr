\set database_name normalized__strong_normalization__person_address
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
    email VARCHAR(50)
);

CREATE TABLE address (
    id int,
    person_id int,
    street VARCHAR(50),
    city VARCHAR(50),
    state VARCHAR(50),
    zip VARCHAR(50)
);

ALTER TABLE Only person
    ADD CONSTRAINT person_primary_key PRIMARY KEY (id);

ALTER TABLE Only address
    ADD CONSTRAINT address_primary_key PRIMARY KEY (id);

ALTER TABLE ONLY address
    ADD CONSTRAINT "FKaddressPerson" FOREIGN KEY (person_id) REFERENCES person(id) ON DELETE CASCADE;

COPY person (id, first_name, last_name, email)
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,John,Doe,john.doe@gmail.com
2,Jane,Doe,jane.doe@gmail.com
3,Jim,Doe,jim.doe@gmail.com
\.

COPY address (id, person_id, street, city, state, zip)
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,1,Applestreet 2,New York,New York,10001
2,2,Orangestreet 3,Los Angeles,California,90001
3,3,Cherrystreet 4,Chicago,Illinois,60601
\.
