CREATE TABLE catalog_materials_folders_structure
(
    link_id serial PRIMARY KEY,
    type varchar(254) NOT NULL,
    parent_folder int8 REFERENCES catalog_materials_folders (folder_id) ON DELETE CASCADE,
    child_folder int8 REFERENCES catalog_materials_folders (folder_id) ON DELETE CASCADE,
    child_material int8 REFERENCES catalog_materials (product_id) ON DELETE CASCADE,
    update_date timestamp default now(),
    creation_date timestamp default now()
)