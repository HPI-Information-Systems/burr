\set database_name hierarchy__complete_redundancy__reviewer_1
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = :'database_name' AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS :database_name;
CREATE DATABASE :database_name;
\c :database_name;
SET default_tablespace = '';
SET default_with_oids = false;

CREATE TABLE author (
    aid INT,
    name VARCHAR(50),
    email VARCHAR(50)
);

CREATE TABLE reviewer (
    rid INT,
    name VARCHAR(50),
    area VARCHAR(50)
);

CREATE TABLE person (
    pid INT,
    name VARCHAR(50) NOT NULL
);

ALTER TABLE Only author
    ADD CONSTRAINT author_primary_key PRIMARY KEY (aid);

ALTER TABLE Only reviewer
    ADD CONSTRAINT reviewer_primary_key PRIMARY KEY (rid);

ALTER TABLE Only person
    ADD CONSTRAINT person_primary_key PRIMARY KEY (pid);

