def test_create_user(client):
    response = client.post(
        '/users',
        json={
            'username': 'antonio',
            'email': 'antonio@example.com',
            'password': '123',
        },
    )

    assert response.status_code == 201  # create
    assert response.json() == {
        'username': 'antonio',
        'email': 'antonio@example.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == 200
    assert response.json() == {
        'users': [
            {
                'username': 'antonio',
                'email': 'antonio@example.com',
                'id': 1,
            }
        ]
    }


def test_read_user(client):
    response = client.get('/users/1')

    assert response.status_code == 200
    assert response.json() == {
        'username': 'antonio',
        'email': 'antonio@example.com',
        'id': 1,
    }


def teste_erro_read_user(client):
    response = client.get('/users/0')

    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'chapolin',
            'email': 'chapolin@example.com',
            'password': 'abc',
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        'username': 'chapolin',
        'email': 'chapolin@example.com',
        'id': 1,
    }


def test_erro_update_user(client):
    response = client.put(
        '/users/0',
        json={
            'username': 'chapolin',
            'email': 'chapolin@example.com',
            'password': 'abc',
        },
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == 200
    assert response.json() == {'message': 'User deleted'}


def test_erro_delete_user(client):
    response = client.delete('/users/0')

    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}
