\c postgres
\set database_name attributes__weak_entity__house
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = :'database_name' AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS :database_name;
CREATE DATABASE :database_name;
\c :database_name;

SET default_tablespace = '';
SET default_with_oids = false;

CREATE TABLE hotel (
    id INT,
    name VARCHAR(50)
);

CREATE TABLE room (
    bed_number INT,
    room_number INT,
    hotel_id INT
);

ALTER TABLE hotel ADD CONSTRAINT hotel_primary_key PRIMARY KEY (id);
ALTER TABLE room ADD CONSTRAINT room_primary_key PRIMARY KEY (room_number, hotel_id);

ALTER TABLE room ADD CONSTRAINT FKroomHotel FOREIGN KEY (hotel_id) REFERENCES hotel(id) ON DELETE CASCADE;

COPY hotel (id, name)
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,Hotel1
2,Hotel2
3,Hotel3
\.

COPY room (id, bed_number, room_number, hotel_id)
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,101,1
2,102,1
1,101,2
2,102,2
1,301,3
2,302,3
3,101,3
\.

