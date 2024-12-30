\c postgres
\set database_name attributes__boolean_relation__process
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = :'database_name' AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS :database_name;
CREATE DATABASE :database_name;
\c :database_name;


SET default_tablespace = '';
SET default_with_oids = false;

CREATE TABLE service (
    id int,
    name varchar(50),
    relevant_for_oil_and_gas boolean,
    relevant_for_automotive boolean,
    relevant_for_chemical boolean,
    relevant_for_pharma boolean,
    relevant_for_food boolean,
    relevant_for_retail boolean,
    relevant_for_logistics boolean,
    relevant_for_aviation boolean,
    relevant_for_energy boolean
);

ALTER TABLE ONLY service ADD CONSTRAINT "service_primary_key" PRIMARY KEY (id);

COPY service ("id", "name", "relevant_for_oil_and_gas", "relevant_for_automotive", "relevant_for_chemical", "relevant_for_pharma", "relevant_for_food", "relevant_for_retail", "relevant_for_logistics", "relevant_for_aviation", "relevant_for_energy")
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,Consulting,true,true,true,true,true,true,true,true,true
2,Software Development,false,true,false,false,false,false,false,false,false
3,Hardware Development,false,false,false,false,false,false,false,false,false
4,Pharma Research,false,false,false,true,false,false,false,false,false
5,Food Production,false,false,false,false,true,false,false,false,false
6,Retail,false,false,false,false,false,true,false,false,false
7,Logistics,false,false,false,false,false,false,true,false,false
8,Aviation,false,false,false,false,false,false,false,true,false
9,Energy Production,false,false,false,false,false,false,false,false,true
\.
