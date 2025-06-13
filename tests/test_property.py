from http import HTTPStatus


def test_create_property(client):
    property_data = {
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

    response = client.post('/api/v1/properties', json=property_data)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'id': 1, **property_data}


def test_read_properties(client, property):
    response = client.get('/api/v1/properties')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == [
        {
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
    ]


def test_read_property_availability(client, property, mock_date_today):
    response = client.get(
        '/api/v1/properties/availability',
        params={
            'property_id': property.id,
            'start_date': '2025-06-17',
            'end_date': '2025-06-20',
            'guests_quantity': 1,
        },
    )
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_read_property_availability_raise_error_with_past_date(
    client, property, mock_date_today
):
    response = client.get(
        '/api/v1/properties/availability',
        params={
            'property_id': property.id,
            'start_date': '2025-06-10',
            'end_date': '2025-06-20',
            'guests_quantity': 1,
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT


def test_read_property_availability_raise_error_with_end_smaller_start(
    client, property, mock_date_today
):
    response = client.get(
        '/api/v1/properties/availability',
        params={
            'property_id': property.id,
            'start_date': '2025-06-20',
            'end_date': '2025-06-19',
            'guests_quantity': 1,
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT


def test_property_availability_error_when_dont_exists(
    client, property, mock_date_today
):
    response = client.get(
        '/api/v1/properties/availability',
        params={
            'property_id': property.id + 1,
            'start_date': '2025-06-19',
            'end_date': '2025-06-20',
            'guests_quantity': 1,
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Esta propriedade não existe.'}


def test_property_availability_error_when_capacity_bigger(
    client, property, mock_date_today
):
    response = client.get(
        '/api/v1/properties/availability',
        params={
            'property_id': property.id,
            'start_date': '2025-06-19',
            'end_date': '2025-06-20',
            'guests_quantity': 3,
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        'detail': 'O número de residentes é maior que a capacidade.'
    }


def test_property_availability_error_when_is_unavailable(
    client, property, reservation, mock_date_today
):
    response = client.get(
        '/api/v1/properties/availability',
        params={
            'property_id': property.id,
            'start_date': '2025-06-14',
            'end_date': '2025-06-15',
            'guests_quantity': 1,
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        'detail': 'Está proprieda não está disponível nesse perído'
    }
