from fastapi import APIRouter, HTTPException, status
from database.queries import (GET_FOLDER_BY_FOLDER_ID,
                              GET_ROOT_FOLDERS,
                              GET_CHILD_FOLDERS,
                              GET_PARENT_FOLDERS,
                              CREATE_FOLDER,
                              DELETE_FOLDER,
                              UPDATE_FOLDER)

from database.connector import DatabaseConnector
from schemas.projects import (FolderItem,
                                      FolderInStructureResponseBody,
                                      CreateFolderRequestBody,
                                      CreateFolderResponseBody,
                                      DeleteFolderRequestBody,
                                      DeleteFolderResponseBody,
                                      UpdateFolderRequestBody,
                                      UpdateFolderResponseBody)

router = APIRouter(prefix='/api/projects')


@router.get('/get_folders', response_model=FolderInStructureResponseBody)
async def get_folders_stucture(folder_id: int):
    connection = DatabaseConnector()
    query = GET_FOLDER_BY_FOLDER_ID.format(folder_id=folder_id)
    result = connection.select(query)
    if len(result) == 0:
        raise HTTPException(status_code=400, detail="folder_id not found")

    elif folder_id>=0:
        connection = DatabaseConnector()
        query_child = GET_CHILD_FOLDERS.format(folder_id=folder_id)
        child = connection.select(query_child)

        result_child = []
        for item in child:
            parent = FolderItem(
                folder_id=item[0],
                name=item[1],
                color=item[2]
            )
            result_child.append(parent)

        query_parents = GET_PARENT_FOLDERS.format(folder_id=folder_id)
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
                                             status_code=200)
    else:
        raise HTTPException(status_code=400, detail='bad folder_id')


@router.post('/create_folder', response_model=CreateFolderResponseBody)
async def create_folder(body: CreateFolderRequestBody):
    connection = DatabaseConnector()

    query = GET_FOLDER_BY_FOLDER_ID.format(folder_id=body.parent)

    result = connection.select(query)

    if len(result) == 0:
        raise HTTPException(status_code=400, detail="no such parent exists")

    query = CREATE_FOLDER.format(name=body.name, color=body.color, parent=body.parent)

    connection.execute(query)

    return CreateFolderResponseBody(message='folder create successful')


@router.delete('/delete_folder', response_model=DeleteFolderResponseBody)
async def delete_folder(body: DeleteFolderRequestBody):

    if body.folder_id == 0:
        raise HTTPException(status_code=400, detail="can't delete the root directory")

    connection = DatabaseConnector()
    query = GET_FOLDER_BY_FOLDER_ID.format(folder_id=body.folder_id)
    result = connection.select(query)
    if len(result) == 0:
        raise HTTPException(status_code=400, detail="folder_id not found")

    query = DELETE_FOLDER.format(folder_id=body.folder_id)
    connection.execute(query)
    return DeleteFolderResponseBody(message='delete folder successful')


@router.put('/update_folder', response_model=UpdateFolderResponseBody)
async def update_folder(body: UpdateFolderRequestBody):
    connection = DatabaseConnector()
    query = UPDATE_FOLDER.format(name=body.name, color=body.color, folder_id=body.folder_id)
    connection.execute(query)
    return UpdateFolderResponseBody(message="update folder successful")



