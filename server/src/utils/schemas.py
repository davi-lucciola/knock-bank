from typing import Any
from pydantic import BaseModel, Field


class MessageResponse(BaseModel):
    message: str
    detail: Any | dict = {}


class PaginationResponse[T](BaseModel):
    data: list[T]
    total: int
    pageIndex: int
    pageSize: int
    totalPages: int


class PaginationQuery(BaseModel):
    pageIndex: int | None = Field(ge=1, default=1)
    pageSize: int | None = Field(ge=1, default=10)
