\set database_name attributes__fk_pk_descriptive__receipt
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = :'database_name' AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS :database_name;
CREATE DATABASE :database_name;
\c :database_name;
SET default_tablespace = '';
SET default_with_oids = false;

CREATE TABLE person (
    name VARCHAR(50),
    email VARCHAR(50)
);

CREATE TABLE receipt (
    id int,
    received_by VARCHAR(50),
    date DATE,
    item VARCHAR(50)
);

ALTER TABLE Only person ADD CONSTRAINT person_primary_key PRIMARY KEY (name);

ALTER TABLE Only receipt ADD CONSTRAINT receipt_primary_key PRIMARY KEY (id);

ALTER TABLE ONLY receipt ADD CONSTRAINT "FKpersonName" FOREIGN KEY (received_by) REFERENCES person(name) ON DELETE CASCADE;

COPY person (name, email)
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
John Doe,john.doe@gmail.com
Jane Doe,jane.doe@gmail.com
Jim Doe,jim.doe@gmail.com
\.

COPY receipt (id, received_by, date, item)
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,John Doe,2020-01-01,Ibuprofen
2,John Doe,2022-01-01,Aspirin
3,Jane Doe,2020-01-02,Citerizin
4,Jim Doe,2020-01-03,Paracetamol
\.
