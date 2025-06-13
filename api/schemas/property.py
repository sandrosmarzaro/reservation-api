import datetime
from enum import Enum
from http import HTTPStatus

from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator


class PropertyBase(BaseModel):
    title: str | None = None
    address_street: str | None = None
    address_number: str | None = None
    address_neighborhood: str
    address_city: str
    address_state: str
    country: str | None = None
    rooms: int = Field(
        gt=0, description='Número de quartos deve ser maior que zero.'
    )
    capacity: int = Field(
        gt=0, description='Capacidade da propriedade deve ser maior que zero'
    )
    price_per_night: float = Field(
        gt=0, description='Preço por noite deve ser maior que zero'
    )


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
    max_capacity: int | None = Field(
        default=None,
        gt=0,
        description='Capacidade máxima deve ser maior que zero',
    )
    max_price_per_night: float | None = Field(
        default=None,
        gt=0,
        description='Preço máximo por noite deve ser maior que zero',
    )

    sort_by_capacity: SortDirection | None = None
    sort_by_price: SortDirection | None = None


class PropertyAvailabilityFilters(BaseModel):
    property_id: int
    start_date: datetime.date
    end_date: datetime.date
    guests_quantity: int = Field(
        gt=0, description='Número de pessoas deve ser maior que zero'
    )

    @field_validator('end_date')
    def validate_end_date(cls, v: datetime.date, info) -> datetime.date:
        if start_date := info.data.get('start_date'):
            if v <= start_date:
                raise HTTPException(
                    detail='A data de fim deve ser maior que a de início.',
                    status_code=HTTPStatus.CONFLICT,
                )
        return v

    @field_validator('start_date')
    def validate_start_date(cls, v: datetime.date) -> datetime.date:
        today = datetime.date.today()
        if v < today:
            raise HTTPException(
                detail='A data de check-in não pode ser no passado.',
                status_code=HTTPStatus.CONFLICT,
            )
        return v
