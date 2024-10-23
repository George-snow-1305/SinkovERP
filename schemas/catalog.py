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


class ServiceItem(BaseModel):
    product_id: int
    article: str
    comments: str | None
    name: str | None
    unit: str | None
    standard_minutes_to_complete: int | None
    production_costs: float | None
    markup: int | None
    costs: float | None


class GetServicesResponseBody(BaseModel):
    services: List[ServiceItem]