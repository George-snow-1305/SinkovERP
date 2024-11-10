from fastapi import APIRouter, HTTPException, status
from database.queries.projects import (GET_FOLDER_BY_FOLDER_ID,
                                          GET_ROOT_FOLDERS,
                                          GET_CHILD_FOLDERS,
                                          GET_PARENT_FOLDERS,
                                          CREATE_FOLDER,
                                          DELETE_FOLDER,
                                          UPDATE_FOLDER,
                                        CREATE_PROJECT,
                                       CREATE_SECTION,
                                       GET_PROJECT_BY_ID,
                                       GET_SECTION_BY_ID,
                                       CREATE_JOB,
                                       GET_OPERATION_BY_ID,
                                       GET_OPERATIONS_PRODUCTS,
                                       CREATE_JOB_FROM_OPERATION,
                                       ADD_RESOURCES_FOR_JUST_CREATED_JOB_FROM_OPERATION,
                                       GET_JOB_BY_ID,
                                       CREATE_RESOURCE,
                                       GET_PRODUCT_FROM_INVOICES,
                                       GET_PRODUCT_FROM_MATERIALS,
                                       GET_PRODUCT_FROM_MECHANISMS,
                                       GET_PRODUCT_FROM_SERVICES)

from utils.utils import prepare_values_with_null

from database.connector import DatabaseConnector
from schemas.projects import (FolderItem,
                              FolderInStructureResponseBody,
                              CreateFolderRequestBody,
                              CreateFolderResponseBody,
                              DeleteFolderRequestBody,
                              DeleteFolderResponseBody,
                              UpdateFolderRequestBody,
                              UpdateFolderResponseBody,
                              CreateProjectRequestBody,
                              CreateProjectResponseBody,
                              CreateSectionResponseBody,
                              CreateSectionRequestBody,
                              CreateJobRequestBody,
                              CreateJobResponseBody,
                              CreateJobFromOperationRequestBody,
                              CreateJobFromOperationResponseBody,
                              CreateResourceRequestBody,
                              CreateResourceResponseBody,
                              CreateResourceFromCatalogResponseBody,
                              CreateResourceFromCatalogRequestBody)

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
                                             parents=result_parents[::-1],
                                             child=result_child)
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


@router.post('/create_project', response_model=CreateProjectResponseBody)
async def create_project(body: CreateProjectRequestBody):
    connection = DatabaseConnector()
    query = GET_FOLDER_BY_FOLDER_ID.format(folder_id=body.parent_id)
    result = connection.select(query)
    if len(result) == 0:
        raise HTTPException(status_code=400, detail="parent not found")

    query = CREATE_PROJECT.format(parent_id=body.parent_id,
                                     name=body.name,
                                     customer=prepare_values_with_null(body.customer),
                                     manager=prepare_values_with_null(body.manager),
                                     owner=prepare_values_with_null(body.owner),
                                     type=prepare_values_with_null(body.type),
                                     adress=prepare_values_with_null(body.adress),
                                     status=prepare_values_with_null(body.status),
                                     start_date=prepare_values_with_null(body.start_date),
                                     end_date=prepare_values_with_null(body.end_date)
                                 )

    connection.execute(query)

    return CreateProjectResponseBody(message="create_project successful")


@router.post('/create_section', response_model=CreateSectionResponseBody)
async def create_section(body: CreateSectionRequestBody):
    connection = DatabaseConnector()
    query = GET_PROJECT_BY_ID.format(project_id=body.project_id)
    result = connection.select(query)
    if len(result) == 0:
        raise HTTPException(status_code=400, detail="project not found")

    query = CREATE_SECTION.format(project_id=body.project_id,
                                  name=body.name,
                                  position=body.position
                                 )

    connection.execute(query)

    return CreateProjectResponseBody(message="create_project successful")


@router.post('/create_job', response_model=CreateJobResponseBody)
async def create_job(body: CreateJobRequestBody):
    connection = DatabaseConnector()
    query = GET_SECTION_BY_ID.format(section_id=body.section_id)
    result = connection.select(query)
    if len(result) == 0:
        raise HTTPException(status_code=400, detail="section not found")

    query = CREATE_JOB.format(section_id=body.section_id,
                              name=body.name,
                              unit=prepare_values_with_null(body.unit),
                              position=body.position,
                              total=body.total)

    connection.execute(query)

    return CreateJobResponseBody(message="create job successful")


@router.post('/create_job_from_operation', response_model=CreateJobFromOperationResponseBody)
async def create_job(body: CreateJobFromOperationRequestBody):
    connection = DatabaseConnector()

    query = GET_OPERATION_BY_ID.format(operation_id=body.operation_id)

    operation_raw = connection.select(query)

    query = GET_OPERATIONS_PRODUCTS.format(operation_id=body.operation_id)

    operations_products_raw = connection.select(query)

    # print(operation_raw)
    #
    # print(operations_products_raw)

    queries = []

    print(operation_raw)

    queries.append(CREATE_JOB_FROM_OPERATION.format(
        section_id=body.section_id,
        position=body.position,
        name=operation_raw[0][1],
        total=operation_raw[0][2]*body.total,
        unit=prepare_values_with_null(operation_raw[0][3]),
        operation_id=operation_raw[0][0]
    ))

    for product in operations_products_raw:

        print(product)
        queries.append(ADD_RESOURCES_FOR_JUST_CREATED_JOB_FROM_OPERATION.format(
            type=product[1],
            name=product[2],
            total=product[3]*body.total,
            unit=prepare_values_with_null(product[4]),
            uint_price=product[5],
            unit_price_for_client=product[6],
            is_from_catalog=True,
            product_id=product[0],
        ))

    connection.execute_in_transaction(queries)

    return CreateJobFromOperationResponseBody(message="Job created successful")


@router.post('/create_resource', response_model=CreateResourceResponseBody)
async def create_resource(body: CreateResourceRequestBody):
    connection = DatabaseConnector()

    query = GET_JOB_BY_ID.format(job_id=body.job_id)

    result = connection.select(query)

    if len(result) == 0:
        raise HTTPException(status_code=400, detail="job not found")

    query = CREATE_RESOURCE.format(
        type=body.type,
        name=body.name,
        total=body.total,
        unit=body.unit,
        unit_price=body.unit_price,
        unit_price_for_client=body.unit_price_for_client,
    )

    connection.execute(query)


@router.post('/create_resource_from_catalog', response_model=CreateResourceFromCatalogRequestBody)
async def create_job(body: CreateResourceFromCatalogResponseBody):
    connection = DatabaseConnector()

    query = GET_JOB_BY_ID.format(job_id=body.job_id)

    result = connection.select(query)

    if len(result) == 0:
        raise HTTPException(status_code=400, detail="job not found")

    if body.type == "material":
        query = GET_PRODUCT_FROM_MATERIALS.format(product_id=body.product_id)
    elif body.type == "service":
        query = GET_PRODUCT_FROM_SERVICES.format(product_id=body.product_id)
    elif body.type == "mechanism":
        query = GET_PRODUCT_FROM_MECHANISMS.format(product_id=body.product_id)
    elif body.type == "invoice":
        query = GET_PRODUCT_FROM_INVOICES.format(product_id=body.product_id)
    else:
        raise HTTPException(status_code=400, detail="This type was not found")

    connection.execute(query)

    return CreateResourceFromCatalogRequestBody(message="resource created successful")