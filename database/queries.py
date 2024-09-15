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
   WHERE child_folder = 4

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