\c postgres
\set database_name attributes__composite_attributes__person
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = :'database_name' AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS :database_name;
CREATE DATABASE :database_name;
\c :database_name;

SET default_tablespace = '';
SET default_with_oids = false;

CREATE TABLE person (
    id INTEGER,
    name VARCHAR(50),
    address VARCHAR(500)
);

ALTER TABLE Only person
    ADD CONSTRAINT person_primary_key PRIMARY KEY (id);

-- address is a composite attribute
COPY person (id, name, address)
FROM stdin
WITH (FORMAT csv, DELIMITER ';');
1;John Doe;Applestreet 2, Houston, Texas, 77005, USA
2;Jane Doe;Orangestreet 3, New York, New York, 10001, USA
3;Jim Doe;Cherrystreet 4, Los Angeles, California, 90001, USA
\.
