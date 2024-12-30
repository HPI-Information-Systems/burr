\c postgres
\set database_name attributes__boolean_relation__beverages
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = :'database_name' AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS :database_name;
CREATE DATABASE :database_name;
\c :database_name;


SET default_tablespace = '';
SET default_with_oids = false;

CREATE TABLE beverage (
    id int,
    name varchar(50),
    contains_caffeine boolean,
    contains_sugar boolean,
    contains_alcohol boolean,
    contains_dairy boolean,
    contains_gluten boolean,
    contains_nuts boolean
);

ALTER TABLE ONLY beverage ADD CONSTRAINT "beverage_primary_key" PRIMARY KEY (id);

COPY beverage ("id", "name", "contains_caffeine", "contains_sugar", "contains_alcohol", "contains_dairy", "contains_gluten", "contains_nuts")
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,Coffee,true,false,false,false,false,false
2,Tea,true,false,false,false,false,false
3,Beer,false,true,true,false,false,false
4,Milk,false,true,false,true,false,false
5,Smoothie,false,true,false,true,false,true
6,Water,false,false,false,false,false,false
\.
