\c postgres
\set database_name schema_anomalies__multiple_concepts_same_table__library
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = :'database_name' AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS :database_name;
CREATE DATABASE :database_name;
\c :database_name;

-- DROP SCHEMA IF EXISTS library_denormalized_multiple_concepts_same_table CASCADE;
-- CREATE SCHEMA library_denormalized_multiple_concepts_same_table;
-- SET search_path TO library_denormalized_multiple_concepts_same_table;

SET default_tablespace = '';
SET default_with_oids = false;

CREATE TABLE book (
    "isbn" VARCHAR(50),
    "name" VARCHAR(50),
    "publication_year" INT,
    "copies_available" INT,
    "author" VARCHAR(50),
    "birth_year" INT,
    "nationality" VARCHAR(50),
    "address" VARCHAR(50)
);

ALTER TABLE ONLY book ADD CONSTRAINT "book_primary_key" PRIMARY KEY (isbn);

COPY book ("isbn", "name", "publication_year", "copies_available", "author", "birth_year", "nationality", "address")
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
978-3-16-148410-0,The Book of Books,2010,5,John Doe,1970,USA,Applestreet 2
978-0747532743,Harry Potter and the Philosophers Stone,1997,5,Joanne K Rowling,1965,USA,44-46 Morningside Road
978-0747532744,Harry Potter and the Chamber of Secrets,1999,5,Joanne K Rowling,1965,USA,44-46 Morningside Road
978-1015131453,Lord of the Rings - The two towers,1954,5,J. R. R. Tolkien,1892,Southafrica,20 Northmoor Road
978-1015131412,Lord of the Rings - The fellowship of the ring,1954,10,J. R. R. Tolkien,1892,Southafrica,20 Northmoor Road
\.
