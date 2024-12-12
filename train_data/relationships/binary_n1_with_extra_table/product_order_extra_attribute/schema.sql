\c postgres
\set database_name relationships__binary_n1_with_extra_table__product_order
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

CREATE TABLE order (
    id INT,
    product_name VARCHAR(50),
    price INT
);

CREATE TABLE client_order (
    client_id INT,
    order_id INT,
    date DATE
)

ALTER TABLE client ADD CONSTRAINT client_primary_key PRIMARY KEY (id);
ALTER TABLE order ADD CONSTRAINT order_primary_key PRIMARY KEY (id);
ALTER TABLE client_order ADD CONSTRAINT client_order_primary_key PRIMARY KEY (client_id, order_id);

ALTER TABLE client_order ADD CONSTRAINT FKclient_orderClient FOREIGN KEY (client_id) REFERENCES client(id) ON DELETE CASCADE;
ALTER TABLE client_order ADD CONSTRAINT FKclient_orderOrder FOREIGN KEY (order_id) REFERENCES order(id) ON DELETE CASCADE;

COPY client (id, name, address)
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,John Doe,Applestreet 2
2,Jane Doe,Orangestreet 3
3,Jim Doe,Cherrystreet 4
\.

COPY order (id, product_name, price)
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,Apple,1
2,Orange,2
3,Cherry,3
\.

COPY client_order (client_id, order_id, date)
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,1,2020-01-01
2,2,2020-01-02
3,3,2020-01-03
\.
