from fastapi import APIRouter, HTTPException, status
from database.queries.catalog import (
                                GET_MATERIALS_FOLDER_BY_FOLDER_ID,
                                GET_MATERIALS_CHILD_FOLDERS,
                                GET_MATERIALS_PARENT_FOLDERS,
                                GET_MATERIALS,
                                CREATE_MATERIALS_FOLDER,
                                DELETE_MATERIALS_FOLDER,
                                UPDATE_MATERIALS_FOLDER,
                                GET_SERVICES_FOLDER_BY_FOLDER_ID,
                                GET_SERVICES_CHILD_FOLDERS,
                                GET_SERVICES_PARENT_FOLDERS,
                                CREATE_SERVICES_FOLDER,
                                DELETE_SERVICES_FOLDER,
                                UPDATE_SERVICES_FOLDER,
                                GET_SERVICES,
                                UPDATE_SERVICE,
                                GET_MECHANISMS_FOLDER_BY_FOLDER_ID,
                                GET_MECHANISMS_CHILD_FOLDERS,
                                GET_MECHANISMS_PARENT_FOLDERS,
                                CREATE_MECHANISMS_FOLDER,
                                DELETE_MECHANISMS_FOLDER,
                                UPDATE_MECHANISMS_FOLDER,
                                GET_MECHANISMS,
                                GET_INVOICES_FOLDER_BY_FOLDER_ID,
                                GET_INVOICES_CHILD_FOLDERS,
                                GET_INVOICES_PARENT_FOLDERS,
                                CREATE_INVOICES_FOLDER,
                                DELETE_INVOICES_FOLDER,
                                UPDATE_INVOICES_FOLDER,
                                GET_INVOICE,
)

from database.connector import DatabaseConnector
from schemas.catalog import (
    FolderItem,
    FolderInStructureResponseBody,
    CreateFolderRequestBody,
    CreateFolderResponseBody,
    DeleteFolderRequestBody,
    DeleteFolderResponseBody,
    UpdateFolderRequestBody,
    UpdateFolderResponseBody,
    GetServicesResponseBody,
    ServiceItem,
    UpdateServiceResponseBody,
    MechanismItem,
    GetMechanismsResponseBody,
    GetInvoicesResponseBody,
    InvoiceItem,
    MaterialsItem,
    GetMaterialsResponseBody)

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
                                             child=result_child)
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


@router.get('/services/get_services', response_model=GetServicesResponseBody)
async def get_services(folder_id):
    connection = DatabaseConnector()
    query = GET_SERVICES.format(folder_id=folder_id)
    query_result = connection.select(query)

    print(query_result)

    services=[]
    for item in query_result:
        service = ServiceItem(product_id=item[0],
                              article=item[1],
                              comments=item[2],
                              name=item[3],
                              unit=item[4],
                              standard_minutes_to_complete=item[5],
                              production_costs=item[6],
                              markup=item[7],
                              costs=item[8])
        services.append(service)

    return GetServicesResponseBody(services=services)


@router.put('/services/update_service', response_model=UpdateServiceResponseBody)
async def update_service(body: ServiceItem):
    connection = DatabaseConnector()
    query = UPDATE_SERVICE.format(product_id=f"'{body.product_id}'" if body.product_id is not None else "null",
                                  article=f"'{body.article}'" if body.article is not None else "null",
                                  comments=f"'{body.comments}'" if body.comments is not None else "null",
                                  name=f"'{body.name}'" if body.name is not None else "null",
                                  unit=f"'{body.unit}'" if body.unit is not None else "null",
                                  standard_minutes_to_complete=f"'{body.standard_minutes_to_complete}'" if body.standard_minutes_to_complete is not None else "null",
                                  production_costs=f"'{body.production_costs}'" if body.production_costs is not None else "null",
                                  markup=f"'{body.markup}'" if body.markup is not None else "null",
                                  costs=f"'{body.costs}'" if body.costs is not None else "null")

    connection.execute(query)

    return UpdateServiceResponseBody(message="update service successful")


@router.get('/materials/get_folders', response_model=FolderInStructureResponseBody)
async def materials_get_folders(folder_id: int):
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


@router.get('/materials/get_materials', response_model=GetMaterialsResponseBody)
async def get_materials(folder_id):
    connection = DatabaseConnector()
    query = GET_MATERIALS.format(folder_id=folder_id)
    query_result = connection.select(query)

    print(query_result)

    materials=[]
    for item in query_result:
        material = MaterialsItem(product_id=item[0],
                              article=item[1],
                              comments=item[2],
                              name=item[3],
                              brand=item[4],
                              unit=item[5],
                              production_costs=item[6],
                              markup=item[7],
                              costs=item[8])
        materials.append(material)

    return GetMaterialsResponseBody(materials=materials)


@router.get('/mechanisms/get_folders', response_model=FolderInStructureResponseBody)
async def mechanisms_get_folders(folder_id: int):
    connection = DatabaseConnector()
    query = GET_MECHANISMS_FOLDER_BY_FOLDER_ID.format(folder_id=folder_id)
    result = connection.select(query)
    if len(result) == 0:
        raise HTTPException(status_code=400, detail="folder_id not found")

    elif folder_id >= 0:
        connection = DatabaseConnector()
        query_child = GET_MECHANISMS_CHILD_FOLDERS.format(folder_id=folder_id)
        child = connection.select(query_child)

        result_child = []
        for item in child:
            parent = FolderItem(
                folder_id=item[0],
                name=item[1],
                color=item[2]
            )
            result_child.append(parent)

        query_parents = GET_MECHANISMS_PARENT_FOLDERS.format(folder_id=folder_id)
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


@router.post('/mechanisms/create_folder', response_model=CreateFolderResponseBody)
async def mechanisms_create_folder(body: CreateFolderRequestBody):
    connection = DatabaseConnector()

    query = GET_MECHANISMS_FOLDER_BY_FOLDER_ID.format(folder_id=body.parent)

    result = connection.select(query)

    if len(result) == 0:
        raise HTTPException(status_code=400, detail="no such parent exists")

    query = CREATE_MECHANISMS_FOLDER.format(name=body.name, color=body.color, parent=body.parent)

    connection.execute(query)

    return CreateFolderResponseBody(message='folder create successful')


@router.delete('/mechanisms/delete_folder', response_model=DeleteFolderResponseBody)
async def mechanisms_delete_folder(body: DeleteFolderRequestBody):
    if body.folder_id == 0:
        raise HTTPException(status_code=400, detail="can't delete the root directory")

    connection = DatabaseConnector()
    query = GET_MECHANISMS_FOLDER_BY_FOLDER_ID.format(folder_id=body.folder_id)
    result = connection.select(query)
    if len(result) == 0:
        raise HTTPException(status_code=400, detail="folder_id not found")

    query = DELETE_MECHANISMS_FOLDER.format(folder_id=body.folder_id)
    connection.execute(query)
    return DeleteFolderResponseBody(message='delete folder successful')


@router.put('/mechanisms/update_folder', response_model=UpdateFolderResponseBody)
async def mechanisms_update_folder(body: UpdateFolderRequestBody):
    connection = DatabaseConnector()
    query = UPDATE_MECHANISMS_FOLDER.format(name=body.name, color=body.color, folder_id=body.folder_id)
    connection.execute(query)
    return UpdateFolderResponseBody(message="update folder successful")


@router.get('/mechanisms/get_mechanisms', response_model=GetMechanismsResponseBody)
async def get_mechanisms(folder_id):
    connection = DatabaseConnector()
    query = GET_MECHANISMS.format(folder_id=folder_id)
    query_result = connection.select(query)

    mechanisms=[]
    for item in query_result:
        mechanism = MechanismItem(
            product_id=item[0],
            article=item[1],
            comments=item[2],
            contractor=item[3],
            name=item[4],
            unit=item[5],
            production_costs=item[6],
            markup=item[7],
            costs=item[8])
        mechanisms.append(mechanism)

    return GetMechanismsResponseBody(mechanisms=mechanisms)


@router.get('/invoices/get_folders', response_model=FolderInStructureResponseBody)
async def get_invoices_folders(folder_id: int):
    connection = DatabaseConnector()
    query = GET_INVOICES_FOLDER_BY_FOLDER_ID.format(folder_id=folder_id)
    result = connection.select(query)
    if len(result) == 0:
        raise HTTPException(status_code=400, detail="folder_id not found")

    elif folder_id >= 0:
        connection = DatabaseConnector()
        query_child = GET_INVOICES_CHILD_FOLDERS.format(folder_id=folder_id)
        child = connection.select(query_child)

        result_child = []
        for item in child:
            parent = FolderItem(
                folder_id=item[0],
                name=item[1],
                color=item[2]
            )
            result_child.append(parent)

        query_parents = GET_INVOICES_PARENT_FOLDERS.format(folder_id=folder_id)
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


@router.post('/invoices/create_folder', response_model=CreateFolderResponseBody)
async def invoices_create_folder(body: CreateFolderRequestBody):
    connection = DatabaseConnector()

    query = GET_INVOICES_FOLDER_BY_FOLDER_ID.format(folder_id=body.parent)

    result = connection.select(query)

    if len(result) == 0:
        raise HTTPException(status_code=400, detail="no such parent exists")

    query = CREATE_INVOICES_FOLDER.format(name=body.name, color=body.color, parent=body.parent)

    connection.execute(query)

    return CreateFolderResponseBody(message='folder create successful')


@router.delete('/invoices/delete_folder', response_model=DeleteFolderResponseBody)
async def invoices_delete_folder(body: DeleteFolderRequestBody):
    if body.folder_id == 0:
        raise HTTPException(status_code=400, detail="can't delete the root directory")

    connection = DatabaseConnector()
    query = GET_INVOICES_FOLDER_BY_FOLDER_ID.format(folder_id=body.folder_id)
    result = connection.select(query)
    if len(result) == 0:
        raise HTTPException(status_code=400, detail="folder_id not found")

    query = DELETE_INVOICES_FOLDER.format(folder_id=body.folder_id)
    connection.execute(query)
    return DeleteFolderResponseBody(message='delete folder successful')


@router.put('/invoices/update_folder', response_model=UpdateFolderResponseBody)
async def invoices_update_folder(body: UpdateFolderRequestBody):
    connection = DatabaseConnector()
    query = UPDATE_INVOICES_FOLDER.format(name=body.name, color=body.color, folder_id=body.folder_id)
    connection.execute(query)
    return UpdateFolderResponseBody(message="update folder successful")


@router.get('/invoices/get_invoices', response_model=GetInvoicesResponseBody)
async def get_invoices(folder_id):
    connection = DatabaseConnector()
    query = GET_INVOICE.format(folder_id=folder_id)
    query_result = connection.select(query)

    invoices=[]
    for item in query_result:
        invoice = InvoiceItem(product_id=item[0],
                                article=item[1],
                                comments=item[2],
                                contractor=item[3],
                                name=item[4],
                                unit=item[5],
                                production_costs=item[6],
                                markup=item[7],
                                costs=item[8])
        invoices.append(invoice)

    return GetInvoicesResponseBody(invoices=invoices)