from typing import Generic, List, TypeVar

from pydantic import BaseModel

M = TypeVar("M")


class PaginatedResponse(BaseModel, Generic[M]):
    data: List[M] = []
    next_page_token: str = ""
    has_more: bool = False
