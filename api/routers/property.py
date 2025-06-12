from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..crud.property import PropertyCRUD
from ..db.database import get_session
from ..schemas.property import (
    PropertyCreate,
    PropertyFilters,
    PropertyResponse,
)

router = APIRouter()


@router.post(
    '/api/v1/properties',
    response_model=PropertyResponse,
    status_code=HTTPStatus.CREATED,
)
def create_property(
    request: PropertyCreate,
    session: Session = Depends(get_session),
):
    return PropertyCRUD.create_property(session=session, request=request)


@router.get(
    '/api/v1/properties',
    response_model=list[PropertyResponse],
    status_code=HTTPStatus.OK,
)
def read_properties(
    filters: PropertyFilters = Depends(),
    session: Session = Depends(get_session),
):
    return PropertyCRUD.get_available_properties(
        session=session, filters=filters
    )
