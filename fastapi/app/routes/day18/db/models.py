from pydantic import BaseModel


class Order(BaseModel):
    id: int
    region_id: int
    gift_name: str
    quantity: int


class Region(BaseModel):
    id: int
    name: str
