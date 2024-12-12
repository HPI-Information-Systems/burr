\c postgres
\set database_name relationships__binary_one_to_one_two_relations__marriage
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = :'database_name' AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS :database_name;
CREATE DATABASE :database_name;
\c :database_name;

SET default_tablespace = '';
SET default_with_oids = false;

CREATE TABLE person (
    id INT,
    name VARCHAR(50),
    sex VARCHAR(1)
);

CREATE TABLE marriage (
    pers_id INT,
    spouse_id INT
);

ALTER TABLE person ADD CONSTRAINT person_primary_key PRIMARY KEY (id);
ALTER TABLE marriage ADD CONSTRAINT marriage_primary_key PRIMARY KEY (pers_id);

ALTER TABLE marriage ADD CONSTRAINT FKmarriagePerson FOREIGN KEY (pers_id) REFERENCES person(id) ON DELETE CASCADE;
ALTER TABLE marriage ADD CONSTRAINT FKmarriageSpouse FOREIGN KEY (spouse_id) REFERENCES person(id) ON DELETE CASCADE;

COPY person (id, name,sex)
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,John Doe,M
2,Jane Doe,F
3,Jim Doe,M
4,Jill Doe,F
\.

COPY marriage(pers_id, spouse_id)
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,2
3,4
\.
