CREATE TABLE catalog_materials
(
    product_id serial PRIMARY KEY,
    article varchar(254),
    comments text,
    brand varchar(254),
    name varchar(254) NOT NULL,
    unit varchar(254),
    production_costs double precision,
    markup double precision,
    costs double precision
);