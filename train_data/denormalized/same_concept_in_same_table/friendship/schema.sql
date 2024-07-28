\set database_name denormalized_same_concept_in_same_table__friendship
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = :'database_name' AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS :database_name;
CREATE DATABASE :database_name;
\c :database_name;

SET default_tablespace = '';
SET default_with_oids = false;

CREATE TABLE friendship (
    "person_id_A" VARCHAR(50),
    "name_A" VARCHAR(50),
    "address_A" VARCHAR(50),
    "person_id_B" VARCHAR(50),
    "name_B" VARCHAR(50),
    "address_B" VARCHAR(50)
);

ALTER TABLE ONLY friendship ADD CONSTRAINT "friendship_primary_key" PRIMARY KEY ("person_id_A", "person_id_B");

COPY friendship ("person_id_A", "name_A", "address_A", "person_id_B", "name_B", "address_B")
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,John Doe,Applestreet 2,2,Jane Doe,Orangestreet 3
2,Jane Doe,Orangestreet 3,3,Jim Doe,Cherrystreet 4
3,Jim Doe,Cherrystreet 4,4,Jill Doe,Strawberrystreet 5
\.
