from pydantic import BaseModel
from typing import Any, List


class FolderItem(BaseModel):
    folder_id: int
    name: str
    color: str


class FolderInStructureResponseBody(BaseModel):
    folder_id: int
    parents: List[FolderItem]
    child: List[FolderItem]


class CreateFolderRequestBody(BaseModel):
    parent: int | None
    name: str
    color: str


class CreateFolderResponseBody(BaseModel):
    message: str


class DeleteFolderRequestBody(BaseModel):
    folder_id: int


class DeleteFolderResponseBody(BaseModel):
    message: str


class UpdateFolderResponseBody(BaseModel):
    message: str


class UpdateFolderRequestBody(BaseModel):
    folder_id: int
    name: str
    color: str


class CreateProjectResponseBody(BaseModel):
    message: str


class CreateProjectRequestBody(BaseModel):
    parent_id: int
    name: str
    customer: str | None
    manager: str | None
    owner: str | None
    type: str | None
    adress: str | None
    status: str | None
    start_date: str | None
    end_date: str | None


class CreateSectionRequestBody(BaseModel):
    project_id: int
    name: str
    position: int


class CreateSectionResponseBody(BaseModel):
    message: str


class CreateJobRequestBody(BaseModel):
    section_id: int
    name: str
    total: int
    unit: str | None
    position: int


class CreateJobResponseBody(BaseModel):
    message: str


class CreateJobFromOperationRequestBody(BaseModel):
    section_id: int
    operation_id: int
    total: float
    position: int


class CreateJobFromOperationResponseBody(BaseModel):
    message: str


class CreateResourceFromCatalogRequestBody(BaseModel):
    job_id: int
    type: str
    product_id: int


class CreateResourceFromCatalogResponseBody(BaseModel):
    message: str


class CreateResourceRequestBody(BaseModel):
    job_id: int
    type: str
    name: str
    total: float
    unit: str
    unit_price: float
    unit_price_for_client: float


class CreateResourceResponseBody(BaseModel):
    message: str