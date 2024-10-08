from fastapi import APIRouter, HTTPException, status
from database.queries.catalog import (
                                GET_MATERIALS_FOLDER_BY_FOLDER_ID,
                                GET_MATERIALS_CHILD_FOLDERS,
                                GET_MATERIALS_PARENT_FOLDERS,
                                CREATE_MATERIALS_FOLDER,
                                DELETE_MATERIALS_FOLDER,
                                UPDATE_MATERIALS_FOLDER,
                                GET_SERVICES_FOLDER_BY_FOLDER_ID,
                                GET_SERVICES_CHILD_FOLDERS,
                                GET_SERVICES_PARENT_FOLDERS,
                                CREATE_SERVICES_FOLDER,
                                DELETE_SERVICES_FOLDER,
                                UPDATE_SERVICES_FOLDER)

from database.connector import DatabaseConnector
from schemas.catalog import (
    FolderItem,
    FolderInStructureResponseBody,
    CreateFolderRequestBody,
    CreateFolderResponseBody,
    DeleteFolderRequestBody,
    DeleteFolderResponseBody,
    UpdateFolderRequestBody,
    UpdateFolderResponseBody)

router = APIRouter(prefix='/api/catalog')


@router.get('/services/get_folders', response_model=FolderInStructureResponseBody)
async def services_get_folders_stucture(folder_id: int):
    connection = DatabaseConnector()
    query = GET_SERVICES_FOLDER_BY_FOLDER_ID.format(folder_id=folder_id)
    result = connection.select(query)
    if len(result) == 0:
        raise HTTPException(status_code=400, detail="folder_id not found")

    elif folder_id>=0:
        connection = DatabaseConnector()
        query_child = GET_SERVICES_CHILD_FOLDERS.format(folder_id=folder_id)
        child = connection.select(query_child)

        result_child = []
        for item in child:
            parent = FolderItem(
                folder_id=item[0],
                name=item[1],
                color=item[2]
            )
            result_child.append(parent)

        query_parents = GET_SERVICES_PARENT_FOLDERS.format(folder_id=folder_id)
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
                                             parents=result_parents[::-1],
                                             child=result_child,
                                             status_code=200)
    else:
        raise HTTPException(status_code=400, detail='bad folder_id')


@router.post('/services/create_folder', response_model=CreateFolderResponseBody)
async def services_create_folder(body: CreateFolderRequestBody):
    connection = DatabaseConnector()

    query = GET_SERVICES_FOLDER_BY_FOLDER_ID.format(folder_id=body.parent)

    result = connection.select(query)

    if len(result) == 0:
        raise HTTPException(status_code=400, detail="no such parent exists")

    query = CREATE_SERVICES_FOLDER.format(name=body.name, color=body.color, parent=body.parent)

    connection.execute(query)

    return CreateFolderResponseBody(message='folder create successful')

@router.delete('/services/delete_folder', response_model=DeleteFolderResponseBody)
async def services_delete_folder(body: DeleteFolderRequestBody):
    if body.folder_id == 0:
        raise HTTPException(status_code=400, detail="can't delete the root directory")

    connection = DatabaseConnector()
    query = GET_SERVICES_FOLDER_BY_FOLDER_ID.format(folder_id=body.folder_id)
    result = connection.select(query)
    if len(result) == 0:
        raise HTTPException(status_code=400, detail="folder_id not found")

    query = DELETE_SERVICES_FOLDER.format(folder_id=body.folder_id)
    connection.execute(query)
    return DeleteFolderResponseBody(message='delete folder successful')


@router.put('/services/update_folder', response_model=UpdateFolderResponseBody)
async def update_folder(body: UpdateFolderRequestBody):
    connection = DatabaseConnector()
    query = UPDATE_SERVICES_FOLDER.format(name=body.name, color=body.color, folder_id=body.folder_id)
    connection.execute(query)
    return UpdateFolderResponseBody(message="update folder successful")


@router.get('/materials/get_folders', response_model=FolderInStructureResponseBody)
async def materials_update_folder(folder_id: int):
    connection = DatabaseConnector()
    query = GET_MATERIALS_FOLDER_BY_FOLDER_ID.format(folder_id=folder_id)
    result = connection.select(query)
    if len(result) == 0:
        raise HTTPException(status_code=400, detail="folder_id not found")

    elif folder_id >= 0:
        connection = DatabaseConnector()
        query_child = GET_MATERIALS_CHILD_FOLDERS.format(folder_id=folder_id)
        child = connection.select(query_child)

        result_child = []
        for item in child:
            parent = FolderItem(
                folder_id=item[0],
                name=item[1],
                color=item[2]
            )
            result_child.append(parent)

        query_parents = GET_MATERIALS_PARENT_FOLDERS.format(folder_id=folder_id)
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
                                             parents=result_parents[::-1],
                                             child=result_child,
                                             status_code=200)
    else:
        raise HTTPException(status_code=400, detail='bad folder_id')


@router.post('/materials/create_folder', response_model=CreateFolderResponseBody)
async def materials_create_folder(body: CreateFolderRequestBody):
    connection = DatabaseConnector()

    query = GET_MATERIALS_FOLDER_BY_FOLDER_ID.format(folder_id=body.parent)

    result = connection.select(query)

    if len(result) == 0:
        raise HTTPException(status_code=400, detail="no such parent exists")

    query = CREATE_MATERIALS_FOLDER.format(name=body.name, color=body.color, parent=body.parent)

    connection.execute(query)

    return CreateFolderResponseBody(message='folder create successful')


@router.delete('/materials/delete_folder', response_model=DeleteFolderResponseBody)
async def materials_delete_folder(body: DeleteFolderRequestBody):
    if body.folder_id == 0:
        raise HTTPException(status_code=400, detail="can't delete the root directory")

    connection = DatabaseConnector()
    query = GET_MATERIALS_FOLDER_BY_FOLDER_ID.format(folder_id=body.folder_id)
    result = connection.select(query)
    if len(result) == 0:
        raise HTTPException(status_code=400, detail="folder_id not found")

    query = DELETE_MATERIALS_FOLDER.format(folder_id=body.folder_id)
    connection.execute(query)
    return DeleteFolderResponseBody(message='delete folder successful')


@router.put('/materials/update_folder', response_model=UpdateFolderResponseBody)
async def materials_update_folder(body: UpdateFolderRequestBody):
    connection = DatabaseConnector()
    query = UPDATE_MATERIALS_FOLDER.format(name=body.name, color=body.color, folder_id=body.folder_id)
    connection.execute(query)
    return UpdateFolderResponseBody(message="update folder successful")
