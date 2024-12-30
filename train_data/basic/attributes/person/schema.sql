\c postgres
\set database_name basic__attributes__person
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = :'database_name' AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS :database_name;
CREATE DATABASE :database_name;
\c :database_name;


SET default_tablespace = '';
SET default_with_oids = false;

CREATE TABLE person (
    id int,
    name VARCHAR(50),
    address VARCHAR(50),
    phone VARCHAR(50)
);

ALTER TABLE Only person
    ADD CONSTRAINT person_primary_key PRIMARY KEY (id);

COPY person (id, name, address, phone)
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,John Doe,Applestreet 2,123456
2,Jane Doe,Orangestreet 3,234567
3,Jim Doe,Cherrystreet 4,345678
\.

