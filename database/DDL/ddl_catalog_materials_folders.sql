CREATE TABLE catalog_materials_folders
(
    folder_id serial PRIMARY KEY,
    name varchar(254) NOT NULL,
    color varchar(254) NOT NULL,
    update_date timestamp default now(),
    creation_date timestamp default now()
)