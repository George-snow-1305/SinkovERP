GET_FOLDER_BY_FOLDER_ID =\
    """SELECT * FROM projects_folders WHERE folder_id = {folder_id}"""


GET_ROOT_FOLDERS =\
    """
    SELECT folder_id, name, color
    FROM projects_folders
    WHERE folder_id in (SELECT parent_folder
    FROM projects_folders_structure
    WHERE parent_folder NOT IN (SELECT child_folder FROM projects_folders_structure  WHERE type = 'folder'))
    """


GET_CHILD_FOLDERS =\
    """
    SELECT folder_id, name, color
    FROM projects_folders
    WHERE folder_id in (SELECT child_folder 
                        FROM projects_folders_structure
                        WHERE parent_folder = {folder_id} and type = 'folder')
    """


GET_PARENT_FOLDERS =\
    """
    WITH RECURSIVE r AS (
   SELECT child_folder, parent_folder
   FROM projects_folders_structure
   WHERE child_folder = {folder_id}

   UNION

   SELECT projects_folders_structure.child_folder, projects_folders_structure.parent_folder
   FROM projects_folders_structure
   JOIN r
        ON projects_folders_structure.child_folder = r.parent_folder
   )

    SELECT parent_folder, name, color FROM r
    LEFT JOIN projects_folders
    ON parent_folder = folder_id;
    """


CREATE_FOLDER =\
    """
    INSERT INTO projects_folders (name, color)
    VALUES ('{name}', '{color}');
    INSERT INTO projects_folders_structure (type, parent_folder, child_folder)
    VALUES ('folder', '{parent}', (SELECT max(folder_id) FROM projects_folders))
    """

DELETE_FOLDER =\
    """
    DELETE FROM projects_folders WHERE folder_id = {folder_id};
    DELETE FROM projects_folders_structure WHERE parent_folder = {folder_id} or child_folder = {folder_id};
    """


UPDATE_FOLDER =\
    """
    UPDATE projects_folders 
    SET name = '{name}', color = '{color}'
    WHERE folder_id = {folder_id}
    """


CREATE_PROJECT =\
    """
    INSERT INTO projects (name, customer, manager, owner, type, adress, status, start_date, end_date)
    VALUES ('{name}', {customer}, {manager}, {owner}, {type}, {adress}, {status}, {start_date}, {end_date});
    INSERT INTO projects_folders_structure (type, parent_folder, child_project)
    VALUES ('project', '{parent_id}', (SELECT max(project_id) FROM projects))
    """


CREATE_SECTION =\
    """
    INSERT INTO projects_sections (name)
    VALUES ('{name}');
    INSERT INTO projects_structure (project_id, position, section_id)
    VALUES ({project_id}, '{position}', (SELECT max(section_id) FROM projects_sections))
    """

GET_PROJECT_BY_ID =\
    """
    SELECT *
    FROM projects
    WHERE project_id = {project_id}
    """


GET_SECTION_BY_ID =\
    """
    SELECT * 
    FROM projects_sections
    WHERE section_id = {section_id}
    """


CREATE_JOB =\
    """
    INSERT INTO projects_jobs (name, total, unit)
    VALUES ('{name}', {total}, {unit});
    INSERT INTO projects_sections_structure (section_id, type, position, job_id)
    VALUES ({section_id}, 'job', {position}, (SELECT max(job_id) FROM projects_jobs))
    """


GET_OPERATION_BY_ID =\
    """
    SELECT operation_id, name, total, unit
    FROM catalog_operations
    WHERE operation_id = {operation_id}
    """


GET_OPERATIONS_PRODUCTS = \
    """
    WITH operations as (SELECT operation_id, type, product_id, total FROM catalog_operations_structure WHERE operation_id = {operation_id})
    
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
    
    UNION ALL
    
    SELECT t2.product_id, type, t2.name, t1.total, t2.unit, t2.production_costs, t2.costs
    FROM operations t1
    LEFT JOIN catalog_services t2
    ON t1.product_id = t2.product_id
    WHERE type = 'service'
    """


CREATE_JOB_FROM_OPERATION =\
    """
    INSERT INTO projects_jobs (name, total, unit, is_from_operation, operation_id)
    VALUES ('{name}', {total}, {unit}, True, {operation_id});
    INSERT INTO projects_sections_structure (section_id, type, position, job_id)
    VALUES ({section_id}, 'job', {position}, (SELECT max(job_id) FROM projects_jobs));
    """

ADD_RESOURCES_FOR_JUST_CREATED_JOB_FROM_OPERATION =\
    """
    INSERT INTO projects_resources (type, name, total, unit, unit_price, unit_price_for_client, is_from_catalog, product_id)
    VALUES ('{type}', '{name}', {total}, {unit}, {uint_price}, {unit_price_for_client}, {is_from_catalog}, {product_id});
    INSERT INTO projects_jobs_structure (job_id, position, resources_id)
    VALUES ((SELECT max(job_id) FROM projects_jobs),
            (SELECT coalesce(max(position), 0) + 1 FROM projects_jobs_structure WHERE job_id = (SELECT max(job_id) FROM projects_jobs)),
            (SELECT max(resource_id) FROM projects_resources))
    """


GET_JOB_BY_ID =\
    """
    SELECT * 
    FROM projects_jobs
    WHERE job_id = {job_id}
    """


CREATE_RESOURCE =\
    """
    INSERT INTO project_recourses (type, name, total, unit, unit_price, unit_price_for_client)
    VALUES ('{type}', '{name}', {total}, {unit}, {unit_price}, {unit_price_for_client})
    INSERT INTO projects_jobs_structure (job_id, position, resource_id)
    VALUES ({job_id}, {position}, {resource_id}})
    """

GET_PRODUCT_FROM_MATERIALS =\
    """
    INSERT projects_resources (type, name, total, unit, unit_price, unit_price_for_client, is_from_catalog, product_id)
    SELECT 'material', name, total, unit, production_costs, costs, True, product_id
    FROM catalog_materials
    WHERE product_id = {product_id};
    INSERT INTO projects_jobs_structure (job_id, position, resource_id)
    VALUES ({job_id}, {position}, {resource_id}})
    """

GET_PRODUCT_FROM_INVOICES =\
    """
    INSERT projects_resources (type, name, total, unit, unit_price, unit_price_for_client, is_from_catalog, product_id)
    SELECT 'invoice', name, total, unit, production_costs, costs, True, product_id
    FROM catalog_invoices
    WHERE product_id = {product_id};
    INSERT INTO projects_jobs_structure (job_id, position, resource_id)
    VALUES ({job_id}, {position}, {resource_id}})
    """

GET_PRODUCT_FROM_MECHANISMS =\
    """
    INSERT projects_resources (type, name, total, unit, unit_price, unit_price_for_client, is_from_catalog, product_id)
    SELECT 'mechanism', name, total, unit, production_costs, costs, True, product_id
    FROM catalog_mechanisms
    WHERE product_id = {product_id};
    INSERT INTO projects_jobs_structure (job_id, position, resource_id)
    VALUES ({job_id}, {position}, {resource_id}})
    """

GET_PRODUCT_FROM_SERVICES =\
    """
    INSERT projects_resources (type, name, total, unit, unit_price, unit_price_for_client, is_from_catalog, product_id)
    SELECT 'service', name, total, unit, production_costs, costs, True, product_id
    FROM catalog_services
    WHERE product_id = {product_id};
    INSERT INTO projects_jobs_structure (job_id, position, resource_id)
    VALUES ({job_id}, {position}, {resource_id}})
    """