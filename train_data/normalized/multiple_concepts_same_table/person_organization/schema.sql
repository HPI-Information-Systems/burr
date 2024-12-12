\c postgres
\set database_name normalized__multiple_concepts_same_table__person_organization
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = :'database_name' AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS :database_name;
CREATE DATABASE :database_name;
\c :database_name;

SET default_tablespace = '';
SET default_with_oids = false;

CREATE TABLE person_organization (
    person_id INTEGER,
    person_name VARCHAR(50),
    person_address VARCHAR(50),
    person_role VARCHAR(50),
    person_phone_number INTEGER,
    organization_id INTEGER,
    organization_name VARCHAR(50),
    organization_address VARCHAR(50),
    organization_phone_number INTEGER    
);

ALTER TABLE Only person_organization
    ADD CONSTRAINT person_organization_primary_key PRIMARY KEY (person_id, organization_id);

COPY person_organization (person_id, person_name, person_address, person_role, person_phone_number, organization_id, organization_name, organization_address, organization_phone_number) 
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,Peter Smith,Platz der Republik 1,Manager,152540479,1,Phone Company,Applestreet 2,01524221234
2,Steve Cook,Kurfürstendamm 31,CEO,123145312,1,Phone Company,Applestreet 2,01524221234
3,Tim Ballmer,Frenchstreet 4,Assistant,321654987,1,Phone Company,Applestreet 2,01524221234
3,Tim Ballmer,Frenchstreet 4,Assistant,321654987,2,Car Manufacturer,Cucumberstreet 2,1221145695
4,Frank Stevens,Rue Charle de Gaulles,Software Engineer,12245214,2,Car Manufacturer,Cucumberstreet 2,1221145695
\.
