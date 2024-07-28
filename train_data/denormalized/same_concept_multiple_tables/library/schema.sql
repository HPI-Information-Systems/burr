\set database_name denormalized__same_concept_multiple_tables__library
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = :'database_name' AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS :database_name;
CREATE DATABASE :database_name;
\c :database_name;

SET default_tablespace = '';
SET default_with_oids = false;

CREATE TABLE book (
    "isbn" VARCHAR(50),
    "name" VARCHAR(50),
    "publication_year" INT,
    "copies_available" INT
);

CREATE TABLE book_2 (
    "isbn" VARCHAR(50),
    "name" VARCHAR(50),
    "publication_year" INT,
    "copies_available" INT
);

ALTER TABLE ONLY book ADD CONSTRAINT "book_primary_key" PRIMARY KEY (isbn);
ALTER TABLE ONLY book_2 ADD CONSTRAINT "book2_primary_key" PRIMARY KEY (isbn);

COPY book ("isbn", "name", "publication_year", "copies_available")
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
978-3-16-148410-0,The Book of Books,2010,5
978-0747532743,Harry Potter and the Philosophers Stone,1997,5
978-0747532744,Harry Potter and the Chamber of Secrets,1999,5
\.


COPY book_2 ("isbn", "name", "publication_year", "copies_available")
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
978-1015131453,Lord of the Rings - The two towers,1954,5
978-1015131412,Lord of the Rings - The fellowship of the ring,1954,10
\.
