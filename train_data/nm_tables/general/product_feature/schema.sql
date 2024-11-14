\c postgres
\set database_name nm_tables__general__product_feature
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = :'database_name' AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS :database_name;
CREATE DATABASE :database_name;
\c :database_name;

CREATE TABLE product (
    id int,
    name varchar(50)
);

CREATE TABLE feature (
    id int,
    name varchar(50)
);

CREATE TABLE product_feature (
    product_id int,
    feature_id int
);

ALTER TABLE ONLY product
    ADD CONSTRAINT product_primary_key PRIMARY KEY (id);

ALTER TABLE ONLY feature
    ADD CONSTRAINT feature_primary_key PRIMARY KEY (id);

ALTER TABLE ONLY product_feature
    ADD CONSTRAINT product_feature_primary_key PRIMARY KEY (product_id, feature_id);

ALTER TABLE ONLY product_feature
    ADD CONSTRAINT "FKproductFeatureProduct" FOREIGN KEY (product_id) REFERENCES product(id) ON DELETE CASCADE;

ALTER TABLE ONLY product_feature
    ADD CONSTRAINT "FKproductFeatureFeature" FOREIGN KEY (feature_id) REFERENCES feature(id) ON DELETE CASCADE;

COPY product ("id", "name")
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,Smartphone
2,Smartwatch
3,Laptop
4,Tablet
5,Waterproof Speaker
6,Basic Phone
\.

COPY feature ("id", "name")
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,WiFi
2,Bluetooth
3,Waterproof
4,Smart
5,Touchscreen
\.


COPY product_feature ("product_id", "feature_id")
FROM stdin
WITH (FORMAT csv, DELIMITER ',');
1,1
1,2
1,3
1,4
1,5
2,1
2,2
2,4
2,5
3,1
3,2
3,4
3,5
4,1
4,2
4,4
4,5
5,1
5,2
5,3
6,NULL
\.
