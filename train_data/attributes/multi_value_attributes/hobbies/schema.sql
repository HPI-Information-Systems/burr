\c postgres
\set database_name attributes__multi_value_attributes__hobbies
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = :'database_name' AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS :database_name;
CREATE DATABASE :database_name;
\c :database_name;


SET default_tablespace = '';
SET default_with_oids = false;

CREATE TABLE person (
    id INT,
    name VARCHAR(50)
);

CREATE TABLE hobbies (
    person_id INT,
    hobby VARCHAR(50)
);

ALTER TABLE Only person
    ADD CONSTRAINT person_primary_key PRIMARY KEY (id);

ALTER TABLE Only hobbies
    ADD CONSTRAINT hobbies_primary_key PRIMARY KEY (person_id, hobby);

ALTER TABLE ONLY hobbies
    ADD CONSTRAINT "FKpersonID" FOREIGN KEY (person_id) REFERENCES person(id) ON DELETE CASCADE;

COPY person (id, name)
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,John Doe
2,Jane Doe
3,Jim Doe
\.

COPY hobbies (person_id, hobby)
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,reading
1,swimming
2,reading
2,swimming
2,cooking
3,reading
3,swimming
3,cooking
3,running
\.
