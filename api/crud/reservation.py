from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..db.models import Property, Reservation, ReservationStatus
from ..schemas.reservation import (
    ReservationCreate,
    ReservationFilters,
)


class ReservationCRUD:
    @staticmethod
    def create_reservation(
        session: Session, request: ReservationCreate
    ) -> Reservation:
        db_reservation = Reservation(**request.model_dump())
        db_property = (
            session.query(Property)
            .filter(Property.id == db_reservation.property_id)
            .first()
        )
        if not db_property:
            raise HTTPException(
                detail='Esta propriedade não existe.',
                status_code=HTTPStatus.NOT_FOUND,
            )

        if db_reservation.guests_quantity > db_property.capacity:
            raise HTTPException(
                detail='O número de residentes é maior que a capacidade.',
                status_code=HTTPStatus.CONFLICT,
            )

        already_reservation_db = (
            session.query(Reservation)
            .filter(
                Reservation.property_id == db_reservation.property_id,
                Reservation.status == ReservationStatus.CONFIRMED,
                Reservation.end_date > db_reservation.start_date,
                Reservation.start_date < db_reservation.end_date,
            )
            .first()
        )
        if already_reservation_db:
            raise HTTPException(
                detail='Propriedade indisponível nesse período.',
                status_code=HTTPStatus.CONFLICT,
            )

        db_reservation.total_price = (
            db_property.price_per_night
            * (db_reservation.end_date - db_reservation.start_date).days
        )

        session.add(db_reservation)
        session.commit()
        session.refresh(db_reservation)

        return db_reservation

    @staticmethod
    def get_reservations(
        session: Session, filters: ReservationFilters
    ) -> list[Reservation]:
        db_reservations = session.query(Reservation)

        if filters.property_id:
            db_reservations = db_reservations.filter(
                Reservation.property_id == filters.property_id
            )

        if filters.client_email:
            db_reservations = db_reservations.filter(
                Reservation.client_email == filters.client_email
            )

        return db_reservations.offset(filters.skip).limit(filters.limit).all()

    @staticmethod
    def patch_reservation_to_cancelled(
        id: int, session: Session
    ) -> Reservation:
        db_reservation = (
            session.query(Reservation).filter(Reservation.id == id).first()
        )
        if not db_reservation:
            raise HTTPException(
                detail='Esta reserva não existe.',
                status_code=HTTPStatus.NOT_FOUND,
            )

        db_reservation.status = ReservationStatus.CANCELLED

        session.add(db_reservation)
        session.commit()
        session.refresh(db_reservation)

        return db_reservation
