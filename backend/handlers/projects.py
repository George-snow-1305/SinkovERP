from fastapi import APIRouter, HTTPException
from backend.database import DatabaseConnector
from backend.schemas.projects import (FolderItem,
                                      FolderInStructureResponseBody,
                                      CreateFolderRequestBody,
                                      CreateFolderResponseBody,
                                      DeleteFolderRequestBody,
                                      DeleteFolderResponseBody,
                                      UpdateFolderRequestBody,
                                      UpdateFolderResponseBody)

router = APIRouter(prefix='/projects')


@router.get('/get_folders', response_model=FolderInStructureResponseBody)
async def get_folders_stucture(folder_id: int):
    if folder_id == 0:
        connection = DatabaseConnector()
        query = """SELECT folder_id, name, color
                    FROM projects_folders
                    WHERE folder_id in (SELECT parent_folder
                    FROM projects_folders_structure
                    WHERE parent_folder NOT IN (SELECT child_folder FROM projects_folders_structure  WHERE type = 'folder'))"""
        result = connection.select(query)
        child = []
        for item in result:
            res = FolderItem(
                folder_id=item[0],
                name=item[1],
                color=item[2]
            )
            child.append(res)

        return FolderInStructureResponseBody(folder_id=folder_id,
                                             parents=[],
                                             child=child,
                                             status_code=200)

    elif folder_id>0:
        connection = DatabaseConnector()
        query_child = f"""SELECT folder_id, name, color
                    FROM projects_folders
                    WHERE folder_id in (SELECT child_folder
                    FROM projects_folders_structure
                    WHERE parent_folder = {folder_id} and type = 'folder')"""
        child = connection.select(query_child)

        result_child = []
        for item in child:
            parent = FolderItem(
                folder_id=item[0],
                name=item[1],
                color=item[2]
            )
            result_child.append(parent)

        query_parents = f"""SELECT folder_id, name, color
                    FROM projects_folders
                    WHERE folder_id in (SELECT parent_folder
                    FROM projects_folders_structure
                    WHERE child_folder = {folder_id} and type = 'folder')"""
        parents = connection.select(query_parents)

        result_parents = []
        for item in parents:
            parent = FolderItem(
                folder_id=item[0],
                name=item[1],
                color=item[2]
            )
            result_parents.append(parent)

        return FolderInStructureResponseBody(folder_id=folder_id,
                                             parents=result_parents,
                                             child=result_child,
                                             status=200)
    else:
        raise HTTPException(status_code=400, detail='bad folder_id')


@router.post('/create_folder', response_model=CreateFolderResponseBody)
async def create_folder(body: CreateFolderRequestBody):
    connection = DatabaseConnector()

    query = f"""INSERT INTO projects_folders (name, color)
        VALUES ('{body.name}', '{body.color}');
        INSERT INTO projects_folders_structure (type, parent_folder, child_folder)
        VALUES ('folder', '{body.parent}', (SELECT max(folder_id) FROM projects_folders))"""
    connection.execute(query)

    return CreateFolderResponseBody(status_code=200)


@router.delete('/delete_folder', response_model=DeleteFolderResponseBody)
async def delete_folder(body: DeleteFolderRequestBody):
    connection = DatabaseConnector()
    query = f"""DELETE FROM projects_folders WHERE folder_id = {body.folder_id}"""
    connection.execute(query)
    return DeleteFolderResponseBody(status_code=200)


@router.put('/update_folder', response_model=UpdateFolderResponseBody)
async def update_folder(body: UpdateFolderRequestBody):
    connection = DatabaseConnector()
    query = f"""UPDATE projects_folders 
                SET name = '{body.name}', color = '{body.color}'
                WHERE folder_id = {body.folder_id}"""
    connection.execute(query)
    return UpdateFolderResponseBody(status_code=200)



