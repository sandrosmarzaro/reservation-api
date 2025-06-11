from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Property(Base):
    __tablename__ = 'properties'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    address_street = Column(String)
    address_number = Column(String)
    address_neighborhood = Column(String, nullable=False)
    address_city = Column(String, nullable=False)
    address_state = Column(String, nullable=False)
    country = Column(String)
    rooms = Column(Integer, nullable=False)
    capacity = Column(Integer, nullable=False)
    price_per_night = Column(Float, nullable=False)

    reservations = relationship('Reservation', back_populates='property')


class Reservation(Base):
    __tablename__ = 'reservations'

    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String, nullable=False)
    client_email = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    guests_quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)

    property_id = Column(Integer, ForeignKey('properties.id'))
    property = relationship('Property', back_populates='reservations')
