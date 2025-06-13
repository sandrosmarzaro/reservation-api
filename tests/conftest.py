import datetime
from contextlib import contextmanager

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from api.db.base import Base
from api.db.database import get_session
from api.db.models import Property, Reservation
from api.main import app


@pytest.fixture
def client(session):
    def get_session_overdrive():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_overdrive
        yield client

        app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)
        engine.dispose()


@contextmanager
def _mock_db_time(*, model, time):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'start_date'):
            target.created_at = datetime(2025, 6, 14)
        if hasattr(target, 'end_date'):
            target.updated_at = datetime(2025, 6, 15)

    event.listen(model, 'before_insert', fake_time_hook)

    yield time

    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def mock_date_today(mocker):
    mock_date = mocker.patch('api.schemas.property.datetime')
    mock_date.date.today.return_value = datetime.date(2025, 6, 12)
    mock_date = mocker.patch('api.schemas.reservation.datetime')
    mock_date.date.today.return_value = datetime.date(2025, 6, 12)


@pytest.fixture
def property(session: Session):
    property_db = Property(
        title='Local',
        address_street='Street',
        address_number='1',
        address_neighborhood='Neighborhood',
        address_city='City',
        address_state='State',
        country='Country',
        rooms=1,
        capacity=2,
        price_per_night=50.0,
    )
    session.add(property_db)
    session.commit()
    session.refresh(property_db)
    return property_db


@pytest.fixture
def reservation(session: Session, property, mock_date_today):
    reservation = Reservation(
        property_id=1,
        client_name='John Doe',
        client_email='john@doe.com',
        start_date=datetime.date(2025, 6, 14),
        end_date=datetime.date(2025, 6, 15),
        guests_quantity=1,
        total_price=50.0
    )
    session.add(reservation)
    session.commit()
    session.refresh(reservation)
    return reservation
