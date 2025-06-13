from http import HTTPStatus

from api.db.models import ReservationStatus


def test_create_reservation(client, property, mock_date_today):
    reservation_data = {
        'property_id': 1,
        'client_name': 'John Doe',
        'client_email': 'john@doe.com',
        'start_date': '2025-06-14',
        'end_date': '2025-06-15',
        'guests_quantity': 1,
    }
    response = client.post('/api/v1/reservations', json=reservation_data)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'total_price': 50.0,
        'status': ReservationStatus.CONFIRMED,
        **reservation_data,
    }


def test_create_reservation_raise_error_when_end_date_smaller(
    client, property, mock_date_today
):
    reservation_data = {
        'property_id': 1,
        'client_name': 'John Doe',
        'client_email': 'john@doe.com',
        'start_date': '2025-06-15',
        'end_date': '2025-06-14',
        'guests_quantity': 1,
    }
    response = client.post('/api/v1/reservations', json=reservation_data)

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        'detail': 'A data de fim deve ser maior que a de início.'
    }


def test_create_reservation_raise_error_when_start_date_past(
    client, property, mock_date_today
):
    reservation_data = {
        'property_id': 1,
        'client_name': 'John Doe',
        'client_email': 'john@doe.com',
        'start_date': '2025-06-11',
        'end_date': '2025-06-14',
        'guests_quantity': 1,
    }
    response = client.post('/api/v1/reservations', json=reservation_data)

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        'detail': 'A data de check-in não pode ser no passado.'
    }


def test_read_reservations(client, reservation):
    response = client.get('/api/v1/reservations')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == [
        {
            'id': 1,
            'total_price': 50.0,
            'status': ReservationStatus.CONFIRMED,
            'property_id': 1,
            'client_email': 'john@doe.com',
            'client_name': 'John Doe',
            'start_date': '2025-06-14',
            'end_date': '2025-06-15',
            'guests_quantity': 1,
        }
    ]


def test_update_reservation_to_cancelled(client, reservation):
    response = client.patch(f'/api/v1/reservations/{reservation.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'total_price': 50.0,
        'status': ReservationStatus.CANCELLED,
        'property_id': 1,
        'client_email': 'john@doe.com',
        'client_name': 'John Doe',
        'start_date': '2025-06-14',
        'end_date': '2025-06-15',
        'guests_quantity': 1,
    }


def test_create_reservation_error_when_property_dont_exist(
    client, reservation
):
    reservation_data = {
        'property_id': reservation.property_id + 1,
        'client_name': 'John Doe',
        'client_email': 'john@doe.com',
        'start_date': '2025-06-14',
        'end_date': '2025-06-15',
        'guests_quantity': 1,
    }
    response = client.post('/api/v1/reservations', json=reservation_data)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Esta propriedade não existe.'}


def test_create_reservation_error_when_capacity_is_bigger(client, reservation):
    reservation_data = {
        'property_id': reservation.property_id,
        'client_name': 'John Doe',
        'client_email': 'john@doe.com',
        'start_date': '2025-06-14',
        'end_date': '2025-06-15',
        'guests_quantity': 3,
    }
    response = client.post('/api/v1/reservations', json=reservation_data)

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        'detail': 'O número de residentes é maior que a capacidade.'
    }


def test_create_reservation_error_when_unavailable(client, reservation):
    reservation_data = {
        'property_id': reservation.property_id,
        'client_name': 'John Doe',
        'client_email': 'john@doe.com',
        'start_date': '2025-06-14',
        'end_date': '2025-06-15',
        'guests_quantity': 1,
    }
    response = client.post('/api/v1/reservations', json=reservation_data)

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        'detail': 'Propriedade indisponível nesse período.'
    }


def test_update_reservations_error_when_dont_exists(client, reservation):
    response = client.patch(f'/api/v1/reservations/{reservation.id + 1}')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Esta reserva não existe.'}


def test_read_reservations_with_id_filter(client, reservation):
    response = client.get('/api/v1/reservations', params={'property_id': 1})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == [
        {
            'id': 1,
            'total_price': 50.0,
            'status': ReservationStatus.CONFIRMED,
            'property_id': 1,
            'client_email': 'john@doe.com',
            'client_name': 'John Doe',
            'start_date': '2025-06-14',
            'end_date': '2025-06-15',
            'guests_quantity': 1,
        }
    ]


def test_read_reservations_with_email_filter(client, reservation):
    response = client.get(
        '/api/v1/reservations',
        params={'client_email': reservation.client_email},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == [
        {
            'id': 1,
            'total_price': 50.0,
            'status': ReservationStatus.CONFIRMED,
            'property_id': 1,
            'client_email': 'john@doe.com',
            'client_name': 'John Doe',
            'start_date': '2025-06-14',
            'end_date': '2025-06-15',
            'guests_quantity': 1,
        }
    ]
