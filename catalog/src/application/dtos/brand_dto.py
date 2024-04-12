from pydantic import BaseModel


class BrandDTO(BaseModel):
    uuid: str
    brand: str
