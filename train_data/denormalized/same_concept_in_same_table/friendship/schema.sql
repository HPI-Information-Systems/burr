\c postgres
\set database_name denormalized__same_concept_in_same_table__friendship
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = :'database_name' AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS :database_name;
CREATE DATABASE :database_name;
\c :database_name;

SET default_tablespace = '';
SET default_with_oids = false;

CREATE TABLE friendship (
    "person_id_a" VARCHAR(50),
    "name_a" VARCHAR(50),
    "address_a" VARCHAR(50),
    "person_id_b" VARCHAR(50),
    "name_b" VARCHAR(50),
    "address_b" VARCHAR(50)
);

ALTER TABLE ONLY friendship ADD CONSTRAINT "friendship_primary_key" PRIMARY KEY ("person_id_a", "person_id_b");

COPY friendship ("person_id_a", "name_a", "address_a", "person_id_b", "name_b", "address_b")
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,John Doe,Applestreet 2,2,Jane Doe,Orangestreet 3
2,Jane Doe,Orangestreet 3,3,Jim Doe,Cherrystreet 4
3,Jim Doe,Cherrystreet 4,4,Jill Doe,Strawberrystreet 5
\.
