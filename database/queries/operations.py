GET_FOLDER_BY_FOLDER_ID =\
    """SELECT * FROM {table_folders} WHERE folder_id = {folder_id}"""


GET_ROOT_FOLDERS =\
    """
    SELECT folder_id, name, color
    FROM {table_folders}
    WHERE folder_id in (SELECT parent_folder
    FROM {table_folders_structure}
    WHERE parent_folder NOT IN (SELECT child_folder FROM {table_folders_structure}  WHERE type = 'folder'))
    """


GET_CHILD_FOLDERS =\
    """
    SELECT folder_id, name, color
    FROM {table_folders}
    WHERE folder_id in (SELECT child_folder 
                        FROM {table_folders_structure}
                        WHERE parent_folder = {folder_id} and type = 'folder')
    """


GET_PARENT_FOLDERS =\
    """
    WITH RECURSIVE r AS (
   SELECT child_folder, parent_folder
   FROM {table_folders_structure}
   WHERE child_folder = {folder_id}

   UNION

   SELECT {table_folders_structure}.child_folder, {table_folders_structure}.parent_folder
   FROM {table_folders_structure}
   JOIN r
        ON {table_folders_structure}.child_folder = r.parent_folder
   )

    SELECT parent_folder, name, color FROM r
    LEFT JOIN {table_folders}
    ON parent_folder = folder_id;
    """


CREATE_FOLDER =\
    """
    INSERT INTO {table_folders} (name, color)
    VALUES ('{name}', '{color}');
    INSERT INTO {table_folders_structure} (type, parent_folder, child_folder)
    VALUES ('folder', '{parent}', (SELECT max(folder_id) FROM {table_folders}))
    """

DELETE_FOLDER =\
    """
    DELETE FROM {table_folders} WHERE folder_id = {folder_id};
    DELETE FROM {table_folders_structure} WHERE parent_folder = {folder_id} or child_folder = {folder_id};
    """


UPDATE_FOLDER =\
    """
    UPDATE {table_folders}
    SET name = '{name}', color = '{color}'
    WHERE folder_id = {folder_id}
    """

CREATE_OPERATION =\
    """
    INSERT INTO {table_operations} (name, total, unit)
    VALUES ('{name}', '{total}', '{unit}');
    INSERT INTO {table_folders_structure} (type, parent_folder, child_operation)
    VALUES ('operation', '{parent}', (SELECT max(operation_id) FROM {table_operations}))
    """

ADD_PRODUCT_TO_OPERATION =\
    """
    INSERT INTO {table_operations_structure} (operation_id, type, product_id, total)
    VALUES ('{operation_id}', '{type}', '{product_id}', '{total}');
    """

GET_OPERATION =\
    """
    SELECT * 
    FROM {table_operations}
    WHERE operation_id = {operation_id}
    """

DELETE_OPERATION =\
    """
    DELETE FROM {table_folders_structure} WHERE child_operation = {operation_id} and type = 'operation';
    DELETE  FROM {table_operations} CASCADE WHERE operation_id = {operation_id};
    DELETE FROM {table_operations_structure} WHERE operation_id = {operation_id}
    """


UPDATE_OPERATION =\
    """
    UPDATE {table_operations}
    SET name = '{name}', unit = '{unit}', total = '{total}'
    WHERE operation_id = {operation_id}
    """

REMOVE_PRODUCT_FROM_OPERATION =\
    """
    DELETE FROM {table_operations_structure}
    WHERE operation_id = {operation_id} and product_id = {product_id} and type = '{type}'
    """

GET_OPERATIONS =\
    """
    WITH operations as (SELECT child_operation as operation_id FROM catalog_operations_folders_structure WHERE parent_folder = {folder_id})

    SELECT t1.operation_id, name, t2.total, unit
    FROM operations t1
    LEFT JOIN  catalog_operations t2
    ON t1.operation_id = t2.operation_id
    """

GET_PRODUCTS_BY_OPERATION =\
    """
    WITH operations as (SELECT operation_id, type, product_id, total FROM catalog_operations_structure WHERE operation_id = {operation_id})

    SELECT t2.product_id, type, t2.name, t1.total, t2.unit, t2.production_costs, t2.costs
    FROM operations t1
    LEFT JOIN catalog_services t2
    ON t1.product_id = t2.product_id
    WHERE type = 'service'
    
    UNION ALL
    
    SELECT t2.product_id, type, t2.name, t1.total, t2.unit, t2.production_costs, t2.costs
    FROM operations t1
    LEFT JOIN catalog_materials t2
    ON t1.product_id = t2.product_id
    WHERE type = 'material'
    
    UNION ALL
    
    SELECT t2.product_id, type, t2.name, t1.total, t2.unit, t2.production_costs, t2.costs
    FROM operations t1
    LEFT JOIN catalog_invoices t2
    ON t1.product_id = t2.product_id
    WHERE type = 'invoice'
    
    UNION ALL
    
    SELECT t2.product_id, type, t2.name, t1.total, t2.unit, t2.production_costs, t2.costs
    FROM operations t1
    LEFT JOIN catalog_mechanisms t2
    ON t1.product_id = t2.product_id
    WHERE type = 'mechanism'
    """

