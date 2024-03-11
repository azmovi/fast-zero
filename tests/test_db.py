from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    new_user = User(username='antonio', password='1234', email='test@test')
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'antonio'))

    assert (
        (user.username == 'antonio')
        and (user.password == '1234')
        and (user.email == 'test@test')
    )
