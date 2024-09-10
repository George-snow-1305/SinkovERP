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
    status_code: int


class CreateFolderRequestBody(BaseModel):
    parent: int | None
    folder_id: int
    name: str
    color: str


class CreateFolderResponseBody(BaseModel):
    status_code: int


class DeleteFolderRequestBody(BaseModel):
    folder_id: int


class DeleteFolderResponseBody(BaseModel):
    status_code: int


class UpdateFolderResponseBody(BaseModel):
    status_code: int


class UpdateFolderRequestBody(BaseModel):
    folder_id: int
    name: str
    color: str
