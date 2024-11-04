CREATE TABLE catalog_operations_structure
(
    link_id serial PRIMARY KEY,
    operation_id int8 REFERENCES catalog_operations (operation_id) ON DELETE CASCADE,
    type varchar(254),
    product_id int8,
    total int8,
    update_date timestamp default now(),
    creation_date timestamp default now()
);