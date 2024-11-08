\set database_name hierarchy__normalized__reviewer_1
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = :'database_name' AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS :database_name;
CREATE DATABASE :database_name;
\c :database_name;


SET default_tablespace = '';
SET default_with_oids = false;

CREATE TABLE person (
    pid INT,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE author (
    pid INT,
    email VARCHAR(50)
);

CREATE TABLE reviewer (
    pid INT,
    area VARCHAR(50)
);


ALTER TABLE Only author
    ADD CONSTRAINT author_primary_key PRIMARY KEY (pid);

ALTER TABLE Only reviewer
    ADD CONSTRAINT reviewer_primary_key PRIMARY KEY (pid);

ALTER TABLE Only person
    ADD CONSTRAINT person_primary_key PRIMARY KEY (pid);

ALTER TABLE ONLY author
    ADD CONSTRAINT "FKpID" FOREIGN KEY (pid) REFERENCES person(pid) ON DELETE CASCADE;

ALTER TABLE ONLY reviewer
    ADD CONSTRAINT "FKpID" FOREIGN KEY (pid) REFERENCES person(pid) ON DELETE CASCADE;


