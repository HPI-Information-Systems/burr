\set database_name attributes__table_checks__adult
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = :'database_name' AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS :database_name;
CREATE DATABASE :database_name;
\c :database_name;
SET default_tablespace = '';
SET default_with_oids = false;

CREATE TABLE adult (
    id INT,
    name VARCHAR(50),
    age INT
)

ALTER TABLE Only adult
    ADD CONSTRAINT adult_primary_key PRIMARY KEY (id);

-- add constraint that age must be over 18
ALTER TABLE ONLY adult
    ADD CONSTRAINT "adult_age_check" CHECK (age >= 18);

COPY adult (id, name, age)
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,John Doe,20
2,Jane Doe,25
3,Jim Doe,30
\.
