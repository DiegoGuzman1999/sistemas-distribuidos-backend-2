import pytest
from app import create_app, db as _db


@pytest.fixture(scope='session')
def app():
    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SECRET_KEY': 'test-secret',
    }
    application = create_app(test_config)

    with application.app_context():
        _db.create_all()
        yield application
        _db.drop_all()


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def limpiar_tablas(app):
    with app.app_context():
        from app.models import Producto
        from app.models_venta import Venta
        _db.session.query(Venta).delete()
        _db.session.query(Producto).delete()
        _db.session.commit()
    yield


# ── Helper: producto de prueba ────────────────────────────────

@pytest.fixture
def producto_base(app):
    with app.app_context():
        from app.models import Producto
        p = Producto(nombre='Laptop', descripcion='Portátil de prueba',
                     cantidad=10, precio=1500.00)
        _db.session.add(p)
        _db.session.commit()
        return p.id   # devuelve solo el id (seguro fuera del contexto)
