\c postgres
\set database_name normalized__third_normal_form__person_address
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = :'database_name' AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS :database_name;
CREATE DATABASE :database_name;
\c :database_name;
SET default_tablespace = '';
SET default_with_oids = false;

CREATE TABLE person (
    id int,
    address_id int,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(50)
);

CREATE TABLE department (
    id int,
    name VARCHAR(50)
);

CREATE TABLE person_department (
    person_id int,
    department_id int
);

CREATE TABLE address (
    id int,
    street VARCHAR(50),
    house_number VARCHAR(50),
    zip VARCHAR(50)
);

CREATE TABLE location (
    zip VARCHAR(50),
    city VARCHAR(50),
    state VARCHAR(50)
);

ALTER TABLE Only person
    ADD CONSTRAINT person_primary_key PRIMARY KEY (id);

ALTER TABLE Only address
    ADD CONSTRAINT address_primary_key PRIMARY KEY (id);

ALTER TABLE Only location
    ADD CONSTRAINT location_primary_key PRIMARY KEY (zip);

ALTER TABLE Only department
    ADD CONSTRAINT department_primary_key PRIMARY KEY (id);


ALTER TABLE ONLY person
    ADD CONSTRAINT "FKpersonAddress" FOREIGN KEY (address_id) REFERENCES address(id) ON DELETE CASCADE;

ALTER TABLE ONLY person_department
    ADD CONSTRAINT "FKpersonDepartmentPerson" FOREIGN KEY (person_id) REFERENCES person(id) ON DELETE CASCADE;

ALTER TABLE ONLY person_department
    ADD CONSTRAINT "FKpersonDepartmentDepartment" FOREIGN KEY (department_id) REFERENCES department(id) ON DELETE CASCADE;

ALTER TABLE ONLY address
    ADD CONSTRAINT "FKaddressLocation" FOREIGN KEY (zip) REFERENCES location(zip) ON DELETE CASCADE;


COPY department (id, name)
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,HR
2,IT
3,Marketing
\.

COPY location (zip, city, state)
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
12345,Applecity,Applestate
23456,Orangecity,Orangestate
34567,Cherrycity,Cherrystate
\.

COPY address (id, street, house_number, zip)
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,Applestreet,2,12345
2,Orangestreet,3,23456
3,Cherrystreet,4,34567
\.

COPY person (id, address_id, first_name, last_name, email)
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,1,John,Doe,'john.doe@gmail.com'
2,1,Jane,Doe,'jane.doe@mail.de'
3,3,Jim,Doe,'jimdoe@mail.com'
\.

COPY person_department (person_id, department_id)
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,1
2,2
3,1
\.
