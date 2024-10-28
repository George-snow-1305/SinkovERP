CREATE TABLE catalog_operations
(
    product_id serial PRIMARY KEY,
    article varchar(254) NOT NULL,
    comments text,
    contractor text,
    name varchar(254) NOT NULL,
    unit varchar(254),
    production_costs double precision,
    markup double precision,
    costs double precision
);