import pytest
from app import create_app, db as _db


@pytest.fixture(scope='function')
def app():
    """Create application for testing."""
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SECRET_KEY': 'test-secret-key',
    })

    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture(scope='function')
def db(app):
    """Fresh database for each test."""
    return _db


@pytest.fixture(scope='function')
def client(app, db):
    """Test client."""
    return app.test_client()