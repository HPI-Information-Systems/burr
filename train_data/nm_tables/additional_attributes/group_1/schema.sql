\set database_name nm_tables__additional_attributes__group_1
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = :'database_name' AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS :database_name;
CREATE DATABASE :database_name;
\c :database_name;

SET default_tablespace = '';
SET default_with_oids = false;

CREATE TABLE user (
    id integer,
)

CREATE TABLE group (
    id integer,
)

CREATE TABLE user_group (
    uid integer,
    gid integer,
    registration_date integer,
    expiration_duration integer,
    access_rights VARCHAR(50)
)

ALTER TABLE Only user
    ADD CONSTRAINT user_primary_key PRIMARY KEY (id);

ALTER TABLE Only group
    ADD CONSTRAINT group_primary_key PRIMARY KEY (id);

ALTER TABLE ONLY user_group
    ADD CONSTRAINT "enableUserGroupPK" PRIMARY KEY (uid, gid);

ALTER TABLE ONLY user_group
    ADD CONSTRAINT "FKusergroupUser" FOREIGN KEY (uid) REFERENCES user(id) ON DELETE CASCADE;

ALTER TABLE ONLY user_group
    ADD CONSTRAINT "FKusergroupGroup" FOREIGN KEY (gid) REFERENCES group(id) ON DELETE CASCADE;
