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
    parent: int
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
    name: str | None
    color: str | None


class CreateOperationResponseBody(BaseModel):
    message: str


class CreateOperationRequestBody(BaseModel):
    parent_folder: int
    name: str | None
    unit: str | None
    total: int | None


class AddProductToOperationRequestBody(BaseModel):
    operation_id: int
    type: str
    product_id: int
    total: int


class AddProductToOperationResponseBody(BaseModel):
    message: str


class DeleteOperationRequestBody(BaseModel):
    operation_id: int


class DeleteOperationResponseBody(BaseModel):
    message: str


class UpdateOperationResponseBody(BaseModel):
    message: str


class UpdateOperationRequestBody(BaseModel):
    operation_id: int
    name: str
    unit: str | None
    total: int | None


class RemoveProductFromOperationResponseBody(BaseModel):
    message: str


class RemoveProductFromOperationRequestBody(BaseModel):
    operation_id: int
    type: str
    product_id: int


class ProductItem(BaseModel):
    type: str
    product_id: int
    name: str | None
    total: int
    unit: str | None
    production_costs: float | None
    costs: float | None


class OperationItem(BaseModel):
    operation_id: int
    name: str
    total: int | None
    unit: str | None
    production_costs: float | None
    costs: float | None
    products: List[ProductItem]


class GetOperationsResponseBody(BaseModel):
    operations: List[OperationItem] | List

