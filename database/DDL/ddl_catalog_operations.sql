create table catalog_operations
(
    operation_id       serial
        primary key,
    name varchar(254) not null,
    total          varchar(254)
);