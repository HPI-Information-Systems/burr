\set database_name nm_tables__trinary_relation__student_intructor_1
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = :'database_name' AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS :database_name;
CREATE DATABASE :database_name;
\c :database_name;

SET default_tablespace = '';
SET default_with_oids = false;

CREATE TABLE student (
    id integer,
    name VARCHAR(50)
)

CREATE TABLE instructor (
    id integer,
    name VARCHAR(50),
)

CREATE TABLE course (
    id integer,
    name VARCHAR(50),
    credits integer,
    max_students integer,
)

CREATE TABLE student_course_instructor (
    sid integer,
    iid integer,
    cid integer
)

ALTER TABLE Only user
    ADD CONSTRAINT user_primary_key PRIMARY KEY (id);

ALTER TABLE Only instructor
    ADD CONSTRAINT instructor_primary_key PRIMARY KEY (id);

ALTER TABLE Only course
    ADD CONSTRAINT course_primary_key PRIMARY KEY (id);

ALTER TABLE ONLY student_course_instructor
    ADD CONSTRAINT "student_course_instructorPK" PRIMARY KEY (sid, iid, cid);

ALTER TABLE ONLY student_course_instructor
    ADD CONSTRAINT "FKstudent_course_instructorStudent" FOREIGN KEY (sid) REFERENCES student(id) ON DELETE CASCADE;

ALTER TABLE ONLY student_course_instructor
    ADD CONSTRAINT "FKstudent_course_instructorInstructor" FOREIGN KEY (iid) REFERENCES instructor(id) ON DELETE CASCADE;

ALTER TABLE ONLY student_course_instructor
    ADD CONSTRAINT "FKstudent_course_instructorCourse" FOREIGN KEY (cid) REFERENCES course(id) ON DELETE CASCADE;

COPY instructor (id, name) FROM stdin;
1, Schmidt
2, Wolff
\.

COPY student (id, name) FROM stdin;
1, Peter
2, Franz
\.

COPY course (id, name, credits, max_students) FROM stdin;
1, Computer Science, 6, 120
2, French, 9, 12
3, Mathematics, 6, 15
4, Psychology, 3, 50
\.

COPY student_course_instructor (sid, iid, cid) FROM stdin;
1,2,1
2,2,1
1,1,3
1,2,3
1,2,4
2,2,2
\.