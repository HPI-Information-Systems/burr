\set database_name nm_tables__composite_keys__university_1
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = :'database_name' AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS :database_name;
CREATE DATABASE :database_name;
\c :database_name;

SET default_tablespace = '';
SET default_with_oids = false;

CREATE TABLE student (
    planned_graduation_year integer,
    first_name VARCHAR(50),
    last_name VARCHAR(50)
);

CREATE TABLE course (
    semester VARCHAR(50),
    course_name VARCHAR(100),
    credits INT
);


CREATE TABLE enrollment (
    planned_graduation_year INT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    semester VARCHAR(50),
    course_name VARCHAR(100)
);

ALTER TABLE Only student
    ADD CONSTRAINT student_primary_key PRIMARY KEY (planned_graduation_year, first_name, last_name);

ALTER TABLE Only course
    ADD CONSTRAINT course_primary_key PRIMARY KEY (semester, course_name);

ALTER TABLE ONLY enrollment
    ADD CONSTRAINT enrollment_primary_key PRIMARY KEY (planned_graduation_year, first_name, last_name, semester, course_name);

ALTER TABLE ONLY enrollment
    ADD CONSTRAINT "FKenrollmentStudent" FOREIGN KEY (planned_graduation_year, first_name, last_name) REFERENCES student(planned_graduation_year, first_name, last_name) ON DELETE CASCADE;

ALTER TABLE ONLY enrollment
    ADD CONSTRAINT "FKenrollmentCourse" FOREIGN KEY (semester, course_name) REFERENCES instructor(semester, course_name) ON DELETE CASCADE;

COPY student (planned_graduation_year, first_name, last_name) FROM stdin;
2016, Franz, Koenig
2021, Peter, Dylan 
\.

COPY course (semester, course_name, credits) FROM stdin;
2023, Computer Science, 6
2016, French, 9
2017, Mathematics, 6
2019, Psychology, 3
\.

COPY enrollment (planned_graduation_year, first_name, last_name, semester, course_name) FROM stdin;
2016, Franz, Koenig, 2023, Computer Science
2016, Franz, Koenig, 2019, Psychology
2021, Peter, Dylan, 2023, Computer Science
2021, Peter, Dylan, 2017, Mathematics
\.