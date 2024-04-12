from pydantic import BaseModel


class CategoryDTO(BaseModel):
    uuid: str
    category: str
