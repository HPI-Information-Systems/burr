\set database_name hierarchy__denormalized__reviewer_1
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = :'database_name' AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS :database_name;
CREATE DATABASE :database_name;
\c :database_name;

SET default_tablespace = '';
SET default_with_oids = false;

CREATE TABLE person (
    pid integer,
    name VARCHAR(50) NOT NULL,
    e-mail VARCHAR(50),
    area VARCHAR(50),
    type VARCHAR(50) NOT NULL,
)

ALTER TABLE Only person
    ADD CONSTRAINT person_primary_key PRIMARY KEY (pid);

