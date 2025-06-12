from http import HTTPStatus

from api.db.models import ReservationStatus


def test_create_property(client):
    response = client.post(
        '/api/v1/properties',
        json={
            'title': 'Local',
            'address_street': 'Street',
            'address_number': '1',
            'address_neighborhood': 'Neighborhood',
            'address_city': 'City',
            'address_state': 'State',
            'country': 'Country',
            'rooms': 1,
            'capacity': 2,
            'price_per_night': 50.0,
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'title': 'Local',
        'address_street': 'Street',
        'address_number': '1',
        'address_neighborhood': 'Neighborhood',
        'address_city': 'City',
        'address_state': 'State',
        'country': 'Country',
        'rooms': 1,
        'capacity': 2,
        'price_per_night': 50.0,
    }


def test_create_reservation(client, property):
    response = client.post(
        '/api/v1/reservations',
        json={
            'property_id': 1,
            'client_name': 'John Doe',
            'client_email': 'john@doe.com',
            'start_date': '2025-06-14',
            'end_date': '2025-06-15',
            'guests_quantity': 1,
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'property_id': 1,
        'client_name': 'John Doe',
        'client_email': 'john@doe.com',
        'start_date': '2025-06-14',
        'end_date': '2025-06-15',
        'guests_quantity': 1,
        'total_price': 50.0,
        'status': ReservationStatus.CONFIRMED,
    }
