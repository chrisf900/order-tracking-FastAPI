from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


@dataclass
class PaginatedResultDTO(Generic[T]):
    items: List[T]
    next_cursor: Optional[str] = None
    has_more: bool = False
