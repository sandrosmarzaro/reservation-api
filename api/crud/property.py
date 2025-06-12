from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from ..db.models import Property, Reservation
from ..schemas.property import (
    PropertyAvailabilityFilters,
    PropertyCreate,
    PropertyFilters,
    SortDirection,
)


class PropertyCRUD:
    @staticmethod
    def create_property(session: Session, request: PropertyCreate) -> Property:
        db_property = Property(**request.model_dump())
        session.add(db_property)
        session.commit()
        session.refresh(db_property)

        return db_property

    @staticmethod
    def get_properties(
        session: Session, filters: PropertyFilters
    ) -> list[Property]:
        db_properties = session.query(Property)

        if filters.neighborhood:
            db_properties = db_properties.filter(
                Property.address_neighborhood == filters.neighborhood
            )

        if filters.city:
            db_properties = db_properties.filter(
                Property.address_city == filters.city
            )

        if filters.state:
            db_properties = db_properties.filter(
                Property.address_state == filters.state
            )

        if filters.max_capacity:
            db_properties = db_properties.filter(
                Property.capacity <= filters.max_capacity
            )

        if filters.max_price_per_night:
            db_properties = db_properties.filter(
                Property.price_per_night <= filters.max_price_per_night
            )

        if filters.sort_by_capacity:
            if filters.sort_by_capacity == SortDirection.DESC:
                db_properties = db_properties.order_by(desc(Property.capacity))
            else:
                db_properties = db_properties.order_by(asc(Property.capacity))

        if filters.sort_by_price:
            if filters.sort_by_price == SortDirection.DESC:
                db_properties = db_properties.order_by(
                    desc(Property.price_per_night)
                )
            else:
                db_properties = db_properties.order_by(
                    asc(Property.price_per_night)
                )

        return db_properties.offset(filters.skip).limit(filters.limit).all()

    @staticmethod
    def get_property_availability(
        filters: PropertyAvailabilityFilters, session: Session
    ) -> None:
        db_property = (
            session.query(Property)
            .filter(Property.id == filters.property_id)
            .first()
        )
        if not db_property:
            raise HTTPException(
                detail='Esta propriedade não existe.',
                status_code=HTTPStatus.NOT_FOUND,
            )

        if filters.guests_quantity > db_property.capacity:
            raise HTTPException(
                detail='O número de residentes é maior que a capacidade.',
                status_code=HTTPStatus.CONFLICT,
            )

        already_reservation_db = (
            session.query(Reservation)
            .filter(
                Reservation.property_id == filters.property_id,
                Reservation.end_date > filters.start_date,
                Reservation.start_date < filters.end_date,
            )
            .first()
        )

        if not already_reservation_db:
            return None
        raise HTTPException(
            detail='Está proprieda não está disponível nesse perído',
            status_code=HTTPStatus.CONFLICT,
        )
