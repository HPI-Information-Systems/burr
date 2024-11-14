\c postgres
\set database_name nm_tables__general__employee_skill
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = :'database_name' AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS :database_name;
CREATE DATABASE :database_name;
\c :database_name;

CREATE TABLE employee (
    id int,
    name varchar(50)
);

CREATE TABLE skill (
    id int,
    name varchar(50)
);

CREATE TABLE employee_skill (
    employee_id int,
    skill_id int
);

ALTER TABLE ONLY employee
    ADD CONSTRAINT employee_primary_key PRIMARY KEY (id);

ALTER TABLE ONLY skill
    ADD CONSTRAINT skill_primary_key PRIMARY KEY (id);

ALTER TABLE ONLY employee_skill
    ADD CONSTRAINT employee_skill_primary_key PRIMARY KEY (employee_id, skill_id);

ALTER TABLE ONLY employee_skill
    ADD CONSTRAINT "FKemployeeskillemployee" FOREIGN KEY (employee_id) REFERENCES employee(id) ON DELETE CASCADE;

ALTER TABLE ONLY employee_skill
    ADD CONSTRAINT "FKemployeeskillskill" FOREIGN KEY (skill_id) REFERENCES skill(id) ON DELETE CASCADE;

COPY employee ("id", "name")
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,John Doe
2,Jane Smith
3,Mark Brown
4,Linda White
5,James Green
\.


COPY skill ("id", "name")
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,Python
2,Java
3,JavaScript
4,SQL
5,Ruby
6,C
7,C++
\.

COPY employee_skill ("employee_id", "skill_id")
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,1
1,2
1,4
2,2
2,3
2,4
2,6
2,7
3,1
3,3
3,4
3,5
4,4
4,5
4,7
5,1
5,2
5,3
5,4
5,5
5,6
5,7
\.