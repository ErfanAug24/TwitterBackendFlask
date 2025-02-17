import json
from typing import Optional
import pytest

from twitter import create_app
import os
import tempfile
from twitter.Config.sqlalchemy_conf import init_tables, db


@pytest.fixture()
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app(testing=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

    with app.app_context():
        init_tables()

    yield app

    with app.app_context():
        db.session.remove()
        # db.drop_all()
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture()
def client(app):
    with app.test_client() as client:
        with app.app_context():
            yield client
            db.session.rollback()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def auth_token(client):
    login_data = {
        "email": "pytest@gmail.com",
        "password": "Py@tests12",
    }
    response = client.post("/login", json=login_data)
    assert response.status_code == 200
    print(response.get_json())
    return response.get_json()["Auth"]["tokens"]
