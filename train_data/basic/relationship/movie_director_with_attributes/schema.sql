\c postgres
\set database_name basic__relationship__movie_director_with_attributes
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = :'database_name' AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS :database_name;
CREATE DATABASE :database_name;
\c :database_name;


SET default_tablespace = '';
SET default_with_oids = false;

CREATE TABLE movie (
    id int,
    title VARCHAR(50),
    director VARCHAR(50),
    year INT
);

CREATE TABLE director (
    name VARCHAR(50),
    birth_year INT
);

ALTER TABLE Only movie
    ADD CONSTRAINT movie_primary_key PRIMARY KEY (id);

ALTER TABLE Only director
    ADD CONSTRAINT director_primary_key PRIMARY KEY (name);

ALTER TABLE ONLY movie
    ADD CONSTRAINT "FKdirector" FOREIGN KEY (director) REFERENCES director(name) ON DELETE CASCADE;

COPY director (name, birth_year)
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
Frank Darabont,1959
Francis Ford Coppola,1939
Christopher Nolan,1970
\.

COPY movie (id, title, director, year)
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,The Shawshank Redemption,Frank Darabont,1994
2,The Godfather,Francis Ford Coppola,1972
3,The Godfather: Part II,Francis Ford Coppola,1974
4,The Dark Knight,Christopher Nolan,2008
\.
