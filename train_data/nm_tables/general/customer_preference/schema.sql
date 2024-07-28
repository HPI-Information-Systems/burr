\set database_name nm_tables__general__smartphone_customer_preference
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = :'database_name' AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS :database_name;
CREATE DATABASE :database_name;
\c :database_name;

CREATE TABLE customer (
    id int,
    name varchar(50)
);

CREATE TABLE preference (
    id int,
    name varchar(50)
);

CREATE TABLE customer_preference (
    customer_id int,
    preference_id int
);

ALTER TABLE ONLY customer
    ADD CONSTRAINT customer_primary_key PRIMARY KEY (id);

ALTER TABLE ONLY preference
    ADD CONSTRAINT preference_primary_key PRIMARY KEY (id);

ALTER TABLE ONLY customer_preference
    ADD CONSTRAINT customer_preference_primary_key PRIMARY KEY (customer_id, preference_id);

ALTER TABLE ONLY customer_preference
    ADD CONSTRAINT "FKcustomerpreferencecustomer" FOREIGN KEY (customer_id) REFERENCES customer(id) ON DELETE CASCADE;

ALTER TABLE ONLY customer_preference
    ADD CONSTRAINT "FKcustomerpreferencepreference" FOREIGN KEY (preference_id) REFERENCES preference(id) ON DELETE CASCADE;

COPY customer ("id", "name")
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,Alice
2,Bob
3,Charlie
4,David
5,Eve
\.

COPY preference ("id", "name")
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,Online Shopping
2,In-Store Shopping
3,Home Delivery
4,Self Pickup
5,Cash Payment
6,Card Payment
7,Digital Wallet
\.

COPY customer_preference ("customer_id", "preference_id")
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,1
1,3
1,6
1,7
2,1
2,2
2,3
2,4
2,5
3,2
3,4
3,5
3,6
4,1
4,2
4,3
4,6
4,7
5,2
5,3
5,5
5,7
\.