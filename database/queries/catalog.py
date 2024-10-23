GET_SERVICES_FOLDER_BY_FOLDER_ID =\
    """SELECT * FROM catalog_services_folders WHERE folder_id = {folder_id}"""


GET_SERVICES_ROOT_FOLDERS =\
    """
    SELECT folder_id, name, color
    FROM catalog_services_folders
    WHERE folder_id in (SELECT parent_folder
    FROM catalog_services_folders_structure
    WHERE parent_folder NOT IN (SELECT child_folder FROM catalog_services_folders_structure  WHERE type = 'folder'))
    """


GET_SERVICES_CHILD_FOLDERS =\
    """
    SELECT folder_id, name, color
    FROM catalog_services_folders
    WHERE folder_id in (SELECT child_folder 
                        FROM catalog_services_folders_structure
                        WHERE parent_folder = {folder_id} and type = 'folder')
    """


GET_SERVICES_PARENT_FOLDERS =\
    """
    WITH RECURSIVE r AS (
   SELECT child_folder, parent_folder
   FROM catalog_services_folders_structure
   WHERE child_folder = {folder_id}

   UNION

   SELECT catalog_services_folders_structure.child_folder, catalog_services_folders_structure.parent_folder
   FROM catalog_services_folders_structure
   JOIN r
        ON catalog_services_folders_structure.child_folder = r.parent_folder
   )

    SELECT parent_folder, name, color FROM r
    LEFT JOIN catalog_services_folders
    ON parent_folder = folder_id;
    """


CREATE_SERVICES_FOLDER =\
    """
    INSERT INTO catalog_services_folders (name, color)
    VALUES ('{name}', '{color}');
    INSERT INTO catalog_services_folders_structure (type, parent_folder, child_folder)
    VALUES ('folder', '{parent}', (SELECT max(folder_id) FROM catalog_services_folders))
    """

DELETE_SERVICES_FOLDER =\
    """
    DELETE FROM catalog_services_folders WHERE folder_id = {folder_id};
    DELETE FROM catalog_services_folders_structure WHERE parent_folder = {folder_id} or child_folder = {folder_id};
    """


UPDATE_SERVICES_FOLDER =\
    """
    UPDATE catalog_services_folders 
    SET name = '{name}', color = '{color}'
    WHERE folder_id = {folder_id}
    """

GET_SERVICES =\
    """
    SELECT product_id,
       article,
       comments,
       name,
       unit,
       standard_minutes_to_complete,
       production_costs,
       markup,
       costs
    FROM catalog_services t1
    LEFT JOIN catalog_services_folders_structure t2
    ON t1.product_id = t2.child_service
    WHERE t2.parent_folder = {folder_id}
    """

GET_MATERIALS_FOLDER_BY_FOLDER_ID =\
    """SELECT * FROM catalog_materials_folders WHERE folder_id = {folder_id}"""


GET_MATERIALS_ROOT_FOLDERS =\
    """
    SELECT folder_id, name, color
    FROM catalog_materials_folders
    WHERE folder_id in (SELECT parent_folder
    FROM catalog_materials_folders_structure
    WHERE parent_folder NOT IN (SELECT child_folder FROM catalog_materials_folders_structure  WHERE type = 'folder'))
    """


GET_MATERIALS_CHILD_FOLDERS =\
    """
    SELECT folder_id, name, color
    FROM catalog_materials_folders
    WHERE folder_id in (SELECT child_folder 
                        FROM catalog_materials_folders_structure
                        WHERE parent_folder = {folder_id} and type = 'folder')
    """


GET_MATERIALS_PARENT_FOLDERS =\
    """
    WITH RECURSIVE r AS (
   SELECT child_folder, parent_folder
   FROM catalog_materials_folders_structure
   WHERE child_folder = {folder_id}

   UNION

   SELECT catalog_materials_folders_structure.child_folder, catalog_materials_folders_structure.parent_folder
   FROM catalog_materials_folders_structure
   JOIN r
        ON catalog_materials_folders_structure.child_folder = r.parent_folder
   )

    SELECT parent_folder, name, color FROM r
    LEFT JOIN catalog_materials_folders
    ON parent_folder = folder_id;
    """


CREATE_MATERIALS_FOLDER =\
    """
    INSERT INTO catalog_materials_folders (name, color)
    VALUES ('{name}', '{color}');
    INSERT INTO catalog_materials_folders_structure (type, parent_folder, child_folder)
    VALUES ('folder', '{parent}', (SELECT max(folder_id) FROM catalog_materials_folders))
    """

DELETE_MATERIALS_FOLDER =\
    """
    DELETE FROM catalog_materials_folders WHERE folder_id = {folder_id};
    DELETE FROM catalog_materials_folders_structure WHERE parent_folder = {folder_id} or child_folder = {folder_id};
    """


UPDATE_MATERIALS_FOLDER =\
    """
    UPDATE catalog_materials_folders 
    SET name = '{name}', color = '{color}'
    WHERE folder_id = {folder_id}
    """

UPDATE_SERVICE =\
    """
    UPDATE catalog_services 
    SET
    article = {article},
    comments = {comments},
    name = {name},
    unit = {unit},
    standard_minutes_to_complete = {standard_minutes_to_complete},
    production_costs = {production_costs},
    markup = {markup},
    costs = {costs}
    WHERE product_id = {product_id}
    """
















