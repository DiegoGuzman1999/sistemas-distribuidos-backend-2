import pytest
from sqlalchemy.pool import StaticPool
from app import create_app, db


@pytest.fixture
def app():
    application = create_app({
        'TESTING': True,
        'SECRET_KEY': 'test-secret',
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_ENGINE_OPTIONS': {
            'connect_args': {'check_same_thread': False},
            'poolclass': StaticPool,
        },
    })

    with application.app_context():
        db.create_all()
        yield application
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def producto_id(client):
    res = client.post('/productos', json={
        'nombre': 'Monitor',
        'descripcion': 'Monitor 24 pulgadas',
        'cantidad': 10,
        'precio': 500.0,
    })
    return res.get_json()['producto']['id']
