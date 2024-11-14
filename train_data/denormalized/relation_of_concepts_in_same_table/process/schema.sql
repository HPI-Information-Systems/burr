\c postgres
\set database_name denormalized__relation_of_concepts_in_same_table__process
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = :'database_name' AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS :database_name;
CREATE DATABASE :database_name;
\c :database_name;

-- DROP SCHEMA IF EXISTS library_denormalized_multiple_concepts_same_table CASCADE;
-- CREATE SCHEMA library_denormalized_multiple_concepts_same_table;
-- SET search_path TO library_denormalized_multiple_concepts_same_table;

SET default_tablespace = '';
SET default_with_oids = false;

CREATE TABLE process (
    process_id int,
    business_area_id int,
    area_name varchar(50),
    area_description varchar(50),
    business_capability_id int,
    capability_name varchar(50),
    capability_description varchar(50)
);

ALTER TABLE ONLY process ADD CONSTRAINT "process_primary_key" PRIMARY KEY (process_id);

COPY process ("process_id", "business_area_id", "area_name", "area_description", "business_capability_id", "capability_name", "capability_description")
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,1,HR,Human Resources,1,Recruitment,Recruitment of new employees
2,1,HR,Human Resources,2,Training,Training of employees
3,2,Finance,Finance,3,Accounting,Accounting of financial transactions
\.
