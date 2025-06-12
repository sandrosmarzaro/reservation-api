from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..crud.reservation import ReservationCRUD
from ..db.database import get_session
from ..schemas.reservation import (
    ReservationCreate,
    ReservationFilters,
    ReservationResponse,
)

router = APIRouter()


@router.post(
    '/api/v1/reservations',
    response_model=ReservationResponse,
    status_code=HTTPStatus.CREATED,
)
def create_reservation(
    request: ReservationCreate,
    session: Session = Depends(get_session),
):
    return ReservationCRUD.create_reservation(session=session, request=request)


@router.get(
    '/api/v1/reservations',
    response_model=list[ReservationResponse],
    status_code=HTTPStatus.OK,
)
def read_reservations(
    filters: ReservationFilters = Depends(),
    session: Session = Depends(get_session),
):
    return ReservationCRUD.get_reservations(session=session, filters=filters)


@router.patch(
    '/api/v1/reservations/{reservation_id}',
    response_model=ReservationResponse,
    status_code=HTTPStatus.OK,
)
def update_reservation_to_cancelled(
    reservation_id: int,
    session: Session = Depends(get_session),
):
    return ReservationCRUD.patch_reservation_to_cancelled(
        reservation_id, session=session
    )
