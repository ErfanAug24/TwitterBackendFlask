import pytest


def test_get_register(client, runner):
    response = client.get("/register")
    assert response.status_code == 405


def test_post_register(client, runner):
    response = client.post(
        "/register",
        json={
            "username": "erfan",
            "fullname": "pytest",
            "email": "eshirkhanei261384@gmail.com",
            "password": "Erfan@261384",
        },
    )
    assert response.status_code == 409  # created once


def test_logout(auth_token, client):
    headers = {"Authorization": f"Bearer {auth_token['access_token']}"}
    response = client.delete("/logout", headers=headers)
    assert response.status_code == 200


def test_refresh(auth_token, client):
    headers = {"Authorization": f"Bearer {auth_token['refresh_token']}"}
    response = client.post("/refresh", headers=headers)
    assert response.get_json()["access_token"] is not None
    assert response.status_code == 200


@pytest.mark.parametrize(
    "username, email, password, fullname, message, field",
    [
        (
            "",
            "erfan@gmail.com",
            "Py@tests12",
            "erfan shirkhani",
            "Username cannot be empty.",
            "username",
        ),
        (
            "mube666",
            "",
            "Py@tests12",
            "erfan shirkhani",
            "Not a valid email address.",
            "email",
        ),
        (
            "mube666",
            "erfan@gmail.com",
            "",
            "erfan shirkhani",
            "Password is invalid.",
            "password",
        ),
        (
            "mube666",
            "erfan@gmail.com",
            "Py@tests12",
            "",
            "Fullname is invalid.",
            "fullname",
        ),
    ],
)
def test_register_validation_input(
    client, username, email, password, fullname, message, field
):
    register_data = {
        "username": username,
        "email": email,
        "fullname": fullname,
        "password": password,
    }
    response = client.post("/register", json=register_data)
    response_json = response.get_json()

    assert message in response_json["errors"][field]


def test_protected(auth_token, client):
    headers = {
        "Authorization": f"Bearer {auth_token['access_token']}",
        "X-CSRF-TOKEN": f"{auth_token['csrf_token']}",
    }
    response = client.get("/protected", headers=headers)
    assert response.status_code == 200
    assert "Access granted with valid CSRF token!" in response.get_json()["message"]
