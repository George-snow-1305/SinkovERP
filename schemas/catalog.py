from pydantic import BaseModel
from typing import Any, List


class FolderItem(BaseModel):
    folder_id: int
    name: str | None
    color: str | None


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


class MaterialsItem(BaseModel):
    product_id: int
    article: str
    comments: str | None
    name: str | None
    brand: str | None
    unit: str | None
    production_costs: float | None
    markup: int | None
    costs: float | None


class GetMaterialsResponseBody(BaseModel):
    materials: List[MaterialsItem]


class UpdateServiceResponseBody(BaseModel):
    message: str


class MechanismItem(BaseModel):
    product_id: int
    article: str
    comments: str | None
    contractor: str| None
    name: str | None
    unit: str | None
    production_costs: float | None
    markup: int | None
    costs: float | None


class GetMechanismsResponseBody(BaseModel):
    mechanisms: List[MechanismItem]


class InvoiceItem(BaseModel):
    product_id: int
    article: str
    comments: str | None
    contractor: str| None
    name: str | None
    unit: str | None
    production_costs: float | None
    markup: int | None
    costs: float | None


class GetInvoicesResponseBody(BaseModel):
    invoices: List[InvoiceItem]