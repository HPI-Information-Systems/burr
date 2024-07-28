\set database_name denormalized__boolean_relation__software
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = :'database_name' AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS :database_name;
CREATE DATABASE :database_name;
\c :database_name;


SET default_tablespace = '';
SET default_with_oids = false;

CREATE TABLE software (
    id int,
    name varchar(50),
    supports_windows boolean,
    supports_mac boolean,
    supports_linux boolean,
);

ALTER TABLE ONLY software ADD CONSTRAINT "software_primary_key" PRIMARY KEY (id);

COPY service ("id", "name", "supports_windows", "supports_mac", "supports_linux")
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,Microsoft Word,true,false,false
2,Microsoft Excel,true,false,false
3,Microsoft Powerpoint,true,false,false
4,Adobe Photoshop,false,true,false
5,Adobe Illustrator,true,true,false
6,Adobe InDesign,true,true,false
7,Adobe Premiere,false,true,false
8,Adobe After Effects,false,true,false
9,Adobe Audition,false,true,true
\.
