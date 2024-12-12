\c postgres
\set database_name hierarchy__each_combination__reviewer_1
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = :'database_name' AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS :database_name;
CREATE DATABASE :database_name;
\c :database_name;

SET default_tablespace = '';
SET default_with_oids = false;

CREATE TABLE person (
    pid INT,
    name VARCHAR(50)
);

CREATE TABLE author (
    pid INT,
    name VARCHAR(50),
    email VARCHAR(50)
);

CREATE TABLE reviewer (
    pid INT,
    name VARCHAR(50),
    area VARCHAR(50)
);

CREATE TABLE author_reviewer (
    pid INT,
    name VARCHAR(50),
    email VARCHAR(50),
    area VARCHAR(50)
);


ALTER TABLE Only person
    ADD CONSTRAINT person_primary_key PRIMARY KEY (pid);

ALTER TABLE Only author
    ADD CONSTRAINT author_primary_key PRIMARY KEY (pid);

ALTER TABLE Only reviewer
    ADD CONSTRAINT reviewer_primary_key PRIMARY KEY (pid);

ALTER TABLE Only author_reviewer
    ADD CONSTRAINT author_reviewer_primary_key PRIMARY KEY (pid);

COPY person(pid, name)
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,John Doe
2,Jane Doe
3,Jim Doe
4,Jill Doe
5,Jack Doe
\.

COPY author(pid, name, email)
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,John Doe,john.doe@email.com
2,Jane Doe,jane.doe@email.com
4,Jill Doe,jill.doe@email.com
\.

COPY reviewer(pid, name, area)
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
3,Jim Doe,Science
4,Jill Doe,Math
\.

COPY author_reviewer(pid, name, email, area)
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
4,Jill Doe,jill.doe@email.com,Math