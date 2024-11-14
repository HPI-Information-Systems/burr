\c postgres
\set database_name basic__table__company
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = :'database_name' AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS :database_name;
CREATE DATABASE :database_name;
\c :database_name;


SET default_tablespace = '';
SET default_with_oids = false;

CREATE TABLE company (
    id int
);

ALTER TABLE Only company
    ADD CONSTRAINT company_primary_key PRIMARY KEY (id);

COPY company (id)
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1
2
3
\.

