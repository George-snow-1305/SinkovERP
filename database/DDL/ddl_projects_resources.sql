create table projects_resources
(
    resource_id           serial
        primary key,
    type                  varchar(254)         not null
        constraint projects_resources_type_check
            check ((type)::text = ANY
                   ((ARRAY ['material'::character varying, 'service'::character varying, 'mechanism'::character varying, 'invoice'::character varying])::text[])),
    name                  varchar(254)         not null,
    total                 double precision,
    unit                  varchar(254),
    unit_price            double precision,
    production_costs      double precision generated always as ((total * unit_price)) stored,
    markup                double precision generated always as ((((unit_price_for_client - unit_price) / unit_price) *
                                                                 (100)::double precision)) stored,
    unit_price_for_client double precision,
    costs_for_client      double precision generated always as ((total * unit_price_for_client)) stored,
    is_from_catalog       boolean              not null,
    product_id            int8,
    is_locked             boolean default true not null
);