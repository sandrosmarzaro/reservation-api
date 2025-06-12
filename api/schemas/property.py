from enum import Enum

from pydantic import BaseModel


class PropertyBase(BaseModel):
    title: str
    address_street: str
    address_number: str
    address_neighborhood: str
    address_city: str
    address_state: str
    country: str
    rooms: int
    capacity: int
    price_per_night: float


class PropertyCreate(PropertyBase):
    pass


class PropertyResponse(PropertyBase):
    id: int

    class Config:
        from_attributes = True


class SortDirection(str, Enum):
    ASC = 'asc'
    DESC = 'desc'


class PropertyFilters(BaseModel):
    skip: int = 0
    limit: int = 10

    neighborhood: str | None = None
    city: str | None = None
    state: str | None = None
    max_capacity: int | None = None
    max_price_per_night: float | None = None

    sort_by_capacity: SortDirection | None = None
    sort_by_price: SortDirection | None = None
