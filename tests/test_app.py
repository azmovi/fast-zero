from fast_zero.schemas import UserPublic


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


def test_error_create_user_existent(client, user):
    response = client.post(
        '/users',
        json={
            'username': 'Test',
            'email': 'test@test.com',
            'password': 'testtest',
        },
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'User already registered'}


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == 200
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == 200
    assert response.json() == {'users': [user_schema]}


def test_read_user_with_id(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/1')

    assert response.status_code == 200
    assert response.json() == user_schema


def teste_erro_read_user_id_index_out_of_range(client):
    response = client.get('/users/0')

    assert response.status_code == 404
    assert response.json() == {'detail': 'User index out of range'}


def teste_erro_read_user_not_found(client):
    response = client.get('/users/2')

    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'chapolin',
            'email': 'chapolin@example.com',
            'password': 'abc',
        },
    )
    user_schema = UserPublic.model_validate(user).model_dump()

    assert response.status_code == 200
    assert response.json() == user_schema


def test_error_update_user_not_enough_permissons(client, user, token):
    response = client.put(
        f'/users/{user.id-1}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'chapolin',
            'email': 'chapolin@example.com',
            'password': 'abc',
        },
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Not enough permissions'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 200
    assert response.json() == {'message': 'User deleted'}


def test_error_delete_user_not_enough_permissons(client, user, token):
    response = client.delete(
        f'/users/{user.id-1}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 400
    assert response.json() == {'detail': 'Not enough permissions'}


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == 200
    assert 'access_token' in token
    assert 'token_type' in token
