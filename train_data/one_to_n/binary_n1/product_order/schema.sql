\c postgres
\set database_name one_to_n__binary_n1__product_order
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = :'database_name' AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS :database_name;
CREATE DATABASE :database_name;
\c :database_name;

SET default_tablespace = '';
SET default_with_oids = false;

CREATE TABLE client (
    id INT,
    name VARCHAR(50),
    address VARCHAR(100)
);

CREATE TABLE product (
    id INT,
    name VARCHAR(50),
    client_id INT,
    price INT
);

ALTER TABLE client ADD CONSTRAINT client_primary_key PRIMARY KEY (id);
ALTER TABLE product ADD CONSTRAINT order_primary_key PRIMARY KEY (id);

ALTER TABLE product ADD CONSTRAINT FKorderClient FOREIGN KEY (client_id) REFERENCES client(id) ON DELETE CASCADE;

COPY client (id, name, address)
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,John Doe,Applestreet 2
2,Jane Doe,Orangestreet 3
3,Jim Doe,Cherrystreet 4
\.

COPY product (id, name, client_id, price)
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,Apple,1,1
2,Orange,2,2
3,Cherry,3,3
4,Olive,1,10
5,Apple,2,1
6,Orange,3,2
7,Cherry,1,3
\.
