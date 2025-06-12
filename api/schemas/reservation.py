import datetime
from http import HTTPStatus

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, field_validator

from api.db.models import ReservationStatus


class ReservationBase(BaseModel):
    property_id: int
    client_name: str
    client_email: EmailStr
    start_date: datetime.date
    end_date: datetime.date
    guests_quantity: int

    @field_validator('end_date')
    def validate_end_date(cls, v: datetime.date, info) -> datetime.time:
        start_date = info.data.get('start_date')
        if start_date and v <= start_date:
            raise HTTPException(
                detail='A data de fim deve ser maior que a de início.',
                status_code=HTTPStatus.CONFLICT,
            )
        return v


class ReservationCreate(ReservationBase):
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
