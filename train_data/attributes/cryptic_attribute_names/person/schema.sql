\set database_name attributes__cryptic_attribute_name__person
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = :'database_name' AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS :database_name;
CREATE DATABASE :database_name;
\c :database_name;
SET default_tablespace = '';
SET default_with_oids = false;


--base32 encoded column names
CREATE TABLE person (
    "NFSA====" int, --id
    "NZQW2ZI=" VARCHAR(50), --name
    "MFTWK===" VARCHAR(50), --age
    "MFSGI4TFONZQ====" VARCHAR(100), --address
    "MVWWC2LM" VARCHAR(50), --email
    "OBUG63TFL5XHK3LCMVZA====" VARCHAR(50) --phone_number
);

ALTER TABLE person ADD CONSTRAINT person_primary_key PRIMARY KEY ("NFSA====");

COPY person ("NFSA====", "NZQW2ZI=", "MFTWK===", "MFSGI4TFONZQ====", "MVWWC2LM", "OBUG63TFL5XHK3LCMVZA====")
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,John Doe,20,Applestreet 2,john.doe@gmail.com,+49132456789
2,Jane Doe,25,Orangestreet 3,jane.doe@gmail.com, +49132426789
3,Jim Doe,30,Cherrystreet 4,jim.doe@gmail.com, +1 132456729
\.
