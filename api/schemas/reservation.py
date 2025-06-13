import datetime
from http import HTTPStatus

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, Field, field_validator

from api.db.models import ReservationStatus


class ReservationBase(BaseModel):
    property_id: int
    client_name: str
    client_email: EmailStr
    start_date: datetime.date
    end_date: datetime.date
    guests_quantity: int = Field(
        gt=0, description='Número de pessoas deve ser maior que zero'
    )


class ReservationCreate(ReservationBase):
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
    pass


class ReservationResponse(ReservationBase):
    id: int
    total_price: float
    status: ReservationStatus

    class Config:
        from_attributes = True


class ReservationFilters(BaseModel):
    skip: int = 0
    limit: int = 10

    property_id: int | None = None
    client_email: EmailStr | None = None
