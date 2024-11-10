from fastapi import APIRouter, HTTPException, status
from database.queries.operations import (GET_FOLDER_BY_FOLDER_ID,
                                          GET_CHILD_FOLDERS,
                                          GET_PARENT_FOLDERS,
                                          CREATE_FOLDER,
                                          DELETE_FOLDER,
                                          UPDATE_FOLDER,
                                          CREATE_OPERATION,
                                         GET_OPERATION,
                                         ADD_PRODUCT_TO_OPERATION,
                                         DELETE_OPERATION,
                                         UPDATE_OPERATION,
                                         REMOVE_PRODUCT_FROM_OPERATION,
                                         GET_OPERATIONS,
                                         GET_PRODUCTS_BY_OPERATION)

from database.connector import DatabaseConnector
from schemas.operations import (
    FolderItem,
    FolderInStructureResponseBody,
    CreateFolderRequestBody,
    CreateFolderResponseBody,
    DeleteFolderRequestBody,
    DeleteFolderResponseBody,
    UpdateFolderRequestBody,
    UpdateFolderResponseBody,
    CreateOperationResponseBody,
    CreateOperationRequestBody,
    AddProductToOperationRequestBody,
    AddProductToOperationResponseBody,
    DeleteOperationRequestBody,
    DeleteOperationResponseBody,
    UpdateOperationRequestBody,
    UpdateOperationResponseBody,
    RemoveProductFromOperationRequestBody,
    RemoveProductFromOperationResponseBody,
    OperationItem,
    ProductItem,
    GetOperationsResponseBody
                                )

router = APIRouter(prefix='/api/catalog/operations')

TABLE_CATALOG_OPERATIONS = "catalog_operations"
TABLE_CATALOG_OPERATIONS_FOLDERS = "catalog_operations_folders"
TABLE_CATALOG_OPERATIONS_FOLDERS_STRUCTURE = "catalog_operations_folders_structure"
TABLE_CATALOG_OPERATIONS_STRUCTURE = "catalog_operations_structure"


@router.get('/get_folders', response_model=FolderInStructureResponseBody)
async def get_folders_stucture(folder_id: int):
    connection = DatabaseConnector()
    query = GET_FOLDER_BY_FOLDER_ID.format(table_folders=TABLE_CATALOG_OPERATIONS_FOLDERS, folder_id=folder_id)
    result = connection.select(query)
    if len(result) == 0:
        raise HTTPException(status_code=400, detail="folder_id not found")

    elif folder_id>=0:
        connection = DatabaseConnector()
        query_child = GET_CHILD_FOLDERS.format(table_folders=TABLE_CATALOG_OPERATIONS_FOLDERS,
                                               table_folders_structure=TABLE_CATALOG_OPERATIONS_FOLDERS_STRUCTURE,
                                               folder_id=folder_id)
        child = connection.select(query_child)
        result_child = []
        for item in child:
            parent = FolderItem(
                folder_id=item[0],
                name=item[1],
                color=item[2]
            )
            result_child.append(parent)

        query_parents = GET_PARENT_FOLDERS.format(table_folders=TABLE_CATALOG_OPERATIONS_FOLDERS,
                                                  table_folders_structure=TABLE_CATALOG_OPERATIONS_FOLDERS_STRUCTURE,
                                                  folder_id=folder_id)
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
                                             child=result_child)
    else:
        raise HTTPException(status_code=400, detail='bad folder_id')


@router.post('/create_folder', response_model=CreateFolderResponseBody)
async def create_folder(body: CreateFolderRequestBody):
    connection = DatabaseConnector()

    query = GET_FOLDER_BY_FOLDER_ID.format(table_folders=TABLE_CATALOG_OPERATIONS_FOLDERS, folder_id=body.parent, )

    result = connection.select(query)

    if len(result) == 0:
        raise HTTPException(status_code=400, detail="no such parent exists")

    query = CREATE_FOLDER.format(name=body.name,
                                 color=body.color,
                                 parent=body.parent,
                                 table_folders=TABLE_CATALOG_OPERATIONS_FOLDERS,
                                 table_folders_structure=TABLE_CATALOG_OPERATIONS_FOLDERS_STRUCTURE
                                 )

    connection.execute(query)

    return CreateFolderResponseBody(message='folder create successful')


@router.delete('/delete_folder', response_model=DeleteFolderResponseBody)
async def delete_folder(body: DeleteFolderRequestBody):

    if body.folder_id == 0:
        raise HTTPException(status_code=400, detail="can't delete the root directory")

    connection = DatabaseConnector()
    query = GET_FOLDER_BY_FOLDER_ID.format(folder_id=body.folder_id,
                                           table_folders=TABLE_CATALOG_OPERATIONS_FOLDERS,
                                           table_folders_structure=TABLE_CATALOG_OPERATIONS_FOLDERS_STRUCTURE
                                           )
    result = connection.select(query)
    if len(result) == 0:
        raise HTTPException(status_code=400, detail="folder_id not found")

    query = DELETE_FOLDER.format(folder_id=body.folder_id,
                                 table_folders=TABLE_CATALOG_OPERATIONS_FOLDERS,
                                 table_folders_structure=TABLE_CATALOG_OPERATIONS_FOLDERS_STRUCTURE
                                 )
    connection.execute(query)
    return DeleteFolderResponseBody(message='delete folder successful')


@router.put('/update_folder', response_model=UpdateFolderResponseBody)
async def update_folder(body: UpdateFolderRequestBody):
    connection = DatabaseConnector()
    query = UPDATE_FOLDER.format(name=body.name,
                                 color=body.color,
                                 folder_id=body.folder_id,
                                 table_folders=TABLE_CATALOG_OPERATIONS_FOLDERS,
                                 table_folders_structure=TABLE_CATALOG_OPERATIONS_FOLDERS_STRUCTURE
                                 )
    connection.execute(query)
    return UpdateFolderResponseBody(message="update folder successful")


@router.post('/create_operation', response_model=CreateOperationResponseBody)
async def create_operation(body: CreateOperationRequestBody):
    connection = DatabaseConnector()

    query = GET_FOLDER_BY_FOLDER_ID.format(table_folders=TABLE_CATALOG_OPERATIONS_FOLDERS, folder_id=body.parent_folder)
    result = connection.select(query)
    if len(result) == 0:
        raise HTTPException(status_code=400, detail="no such parent exists")

    query = CREATE_OPERATION.format(
        table_operations=TABLE_CATALOG_OPERATIONS,
        table_folders_structure=TABLE_CATALOG_OPERATIONS_FOLDERS_STRUCTURE,
        parent=body.parent_folder,
        name=body.name,
        total=body.total,
        unit=body.unit
    )
    print(query)
    connection.execute(query)

    return CreateOperationResponseBody(message='folder create successful')


@router.post('/add_product_to_operation', response_model=AddProductToOperationResponseBody)
async def add_product_to_operation(body: AddProductToOperationRequestBody):
    connection = DatabaseConnector()

    query = GET_OPERATION.format(table_operations=TABLE_CATALOG_OPERATIONS, operation_id=body.operation_id)
    result = connection.select(query)
    if len(result) == 0:
        raise HTTPException(status_code=400, detail="no such operation exists")

    query = ADD_PRODUCT_TO_OPERATION.format(
        table_operations_structure=TABLE_CATALOG_OPERATIONS_STRUCTURE,
        operation_id=body.operation_id,
        type=body.type,
        product_id=body.product_id,
        total=body.total
    )

    connection.execute(query)

    return AddProductToOperationResponseBody(message='product added successful')


@router.delete('/delete_operation', response_model=DeleteOperationResponseBody)
async def delete_operation(body: DeleteOperationRequestBody):
    connection = DatabaseConnector()

    query = GET_OPERATION.format(table_operations=TABLE_CATALOG_OPERATIONS, operation_id=body.operation_id)
    result = connection.select(query)
    if len(result) == 0:
        raise HTTPException(status_code=400, detail="no such operation exists")

    query = DELETE_OPERATION.format(
        table_folders_structure=TABLE_CATALOG_OPERATIONS_FOLDERS_STRUCTURE,
        table_operations_structure=TABLE_CATALOG_OPERATIONS_STRUCTURE,
        table_operations=TABLE_CATALOG_OPERATIONS,
        operation_id=body.operation_id,
    )

    connection.execute(query)

    return DeleteOperationResponseBody(message='operation deleted successful')


@router.put('/update_operation', response_model=UpdateOperationResponseBody)
async def update_operation(body: UpdateOperationRequestBody):
    connection = DatabaseConnector()

    query = GET_OPERATION.format(table_operations=TABLE_CATALOG_OPERATIONS, operation_id=body.operation_id)
    result = connection.select(query)
    if len(result) == 0:
        raise HTTPException(status_code=400, detail="no such operation exists")

    query = UPDATE_OPERATION.format(
        table_operations=TABLE_CATALOG_OPERATIONS,
        operation_id=body.operation_id,
        name=body.name,
        unit=body.unit,
        total=body.total
    )

    connection.execute(query)

    return UpdateOperationResponseBody(message='operation updated successful')


@router.post('/remove_product_from_operation', response_model=RemoveProductFromOperationResponseBody)
async def remove_product_from_operation(body: RemoveProductFromOperationRequestBody):
    connection = DatabaseConnector()

    query = GET_OPERATION.format(table_operations=TABLE_CATALOG_OPERATIONS, operation_id=body.operation_id)
    result = connection.select(query)
    if len(result) == 0:
        raise HTTPException(status_code=400, detail="no such operation exists")

    query = REMOVE_PRODUCT_FROM_OPERATION.format(
        table_operations_structure=TABLE_CATALOG_OPERATIONS_STRUCTURE,
        operation_id=body.operation_id,
        type=body.type,
        product_id=body.product_id
    )

    connection.execute(query)

    return RemoveProductFromOperationResponseBody(message='product remove successful')


@router.get('/get_operations')#, response_model=GetOperationsResponseBody)
async def get_operations(folder_id: int):
    connection = DatabaseConnector()

    query = GET_OPERATIONS.format(table_operations=TABLE_CATALOG_OPERATIONS,
                                  table_operations_structure=TABLE_CATALOG_OPERATIONS_STRUCTURE,
                                  table_folders_structure=TABLE_CATALOG_OPERATIONS_FOLDERS_STRUCTURE,
                                  folder_id=folder_id)
    operations = []

    operations_raw = connection.select(query)
    if len(operations_raw) == 0:
        return GetOperationsResponseBody(operations=[])

    for operation_raw in operations_raw:
        query = GET_PRODUCTS_BY_OPERATION.format(operation_id=operation_raw[0])

        products_raw = connection.select(query)

        products = []

        production_costs=0
        costs=0

        for product_raw in products_raw:
            products.append(
                ProductItem(
                    type=product_raw[1],
                    product_id=product_raw[0],
                    name=product_raw[2],
                    total=product_raw[3],
                    unit=product_raw[4],
                    production_costs=product_raw[5],
                    costs=product_raw[6]
                )
            )

            production_costs+=product_raw[5]
            costs+=product_raw[6]

        operations.append(
            OperationItem(
                operation_id=operation_raw[0],
                name=operation_raw[1],
                total=operation_raw[2],
                unit=operation_raw[3],
                production_costs=production_costs,
                costs=costs,
                products=products
            )
        )

    return GetOperationsResponseBody(operations=operations)



