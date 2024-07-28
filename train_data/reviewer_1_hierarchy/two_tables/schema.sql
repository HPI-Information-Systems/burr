\set database_name hierarchy__two_tables__reviewer_1
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = :'database_name' AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS :database_name;
CREATE DATABASE :database_name;
\c :database_name;
SET default_tablespace = '';
SET default_with_oids = false;

CREATE TABLE author (
    aid int,
    name VARCHAR(50),
    e-mail VARCHAR(50),
)

CREATE TABLE reviewer (
    rid int,
    name VARCHAR(50),
    area VARCHAR(50),
)

ALTER TABLE Only author
    ADD CONSTRAINT author_primary_key PRIMARY KEY (aid);

ALTER TABLE Only reviewer
    ADD CONSTRAINT reviewer_primary_key PRIMARY KEY (rid);

