CREATE TABLE catalog_services
(
    product_id serial PRIMARY KEY,
    article varchar(254),
    comments text,
    name varchar(254) NOT NULL,
    unit varchar(254),
    standard_minutes_to_complete int8,
    production_costs double precision,
    markup double precision,
    costs double precision
);