\c postgres
\set database_name one_to_one__binary_one_to_one_single_relation__marriage
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = :'database_name' AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS :database_name;
CREATE DATABASE :database_name;
\c :database_name;

SET default_tablespace = '';
SET default_with_oids = false;

CREATE TABLE person (
    id INT,
    name VARCHAR(50),
    sex VARCHAR(1),
    spouse_id INT
);

ALTER TABLE person ADD CONSTRAINT person_primary_key PRIMARY KEY (id);
ALTER TABLE person ADD CONSTRAINT person_spouse_id_fkey FOREIGN KEY (spouse_id) REFERENCES person(id) ON DELETE CASCADE;

COPY person
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,John Doe,M,2
2,Jane Doe,F,1
3,Jim Doe,M,4
4,Jill Doe,F,3
\.