from fast_zero.schemas import UserPublic
from tests.factories import UserFactory


def test_create_user(client):
    response = client.post(
        '/users/',
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
        '/users/',
        json={
            'username': f'{user.username}',
            'email': f'{user.email}',
            'password': f'{user.clean_password}',
        },
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Email already registered'}


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == 200
    assert response.json() == {'users': []}


def test_read_users_with_users(client, session):
    users = UserFactory.create_batch(10)
    session.bulk_save_objects(users)
    session.commit()
    users_schema = [
        UserPublic.model_validate(user).model_dump() for user in users
    ]
    response = client.get('/users/')

    assert response.status_code == 200
    assert response.json() == {'users': users_schema}


def test_read_user_with_id(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(f'/users/{user.id}')

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


def test_error_update_user_not_enough_permissons(client, other_user, token):
    response = client.put(
        f'/users/{other_user.id}',
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
    assert response.json() == {'detail': 'User deleted'}


def test_error_delete_user_not_enough_permissons(client, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 400
    assert response.json() == {'detail': 'Not enough permissions'}
