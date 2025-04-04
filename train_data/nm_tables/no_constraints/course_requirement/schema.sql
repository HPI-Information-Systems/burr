\c postgres
\set database_name nm_tables__no_constraints__course_requirement
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = :'database_name' AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS :database_name;
CREATE DATABASE :database_name;
\c :database_name;

CREATE TABLE course (
    id int,
    name varchar(50)
);

CREATE TABLE requirement (
    id int,
    name varchar(50)
);

CREATE TABLE course_requirement (
    course_id int,
    requirement_id int
);

COPY course ("id", "name")
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,Engineering
2,Literature
3,Computer Science
4,Biology
5,History
\.

COPY requirement ("id", "name")
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,Math
2,Science
3,Programming
4,Writing
5,Research
\.

-- Insert data into the course_requirement table
COPY course_requirement ("course_id", "requirement_id")
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,1
1,2
1,3
1,5
2,4
2,5
3,1
3,3
3,5
4,1
4,2
4,4
4,5
5,4
5,5
\.
