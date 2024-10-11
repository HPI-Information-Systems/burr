\set database_name basic__relationship__movie_director_simple
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = :'database_name' AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS :database_name;
CREATE DATABASE :database_name;
\c :database_name;


SET default_tablespace = '';
SET default_with_oids = false;

CREATE TABLE movie (
    id int,
    director int
);

CREATE TABLE director (
    id int
);

ALTER TABLE Only movie
    ADD CONSTRAINT movie_primary_key PRIMARY KEY (id);

ALTER TABLE Only director
    ADD CONSTRAINT director_primary_key PRIMARY KEY (id);

ALTER TABLE ONLY movie
    ADD CONSTRAINT "FKdirector" FOREIGN KEY (director) REFERENCES director(id) ON DELETE CASCADE;

COPY director (id)
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1
2
3
\.

COPY movie (id, director)
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,1
2,2
3,2
4,3
\.
