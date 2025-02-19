from io import BytesIO


def test_upload_image(client, auth_token):
    headers = {
        "Authorization": f"Bearer {auth_token['access_token']}",
        "X-CSRF-TOKEN": f"{auth_token['csrf_token']}",
    }
    data = {"photo": (BytesIO(b"\x89PNG\r\n\x1a\n"), "test_image.png")}
    response = client.post(
        "/user/upload", content_type="multipart/form-data", data=data, headers=headers
    )
    assert response.status_code == 200
    assert response.get_json()["filename"] == "test_image.png"


# def test_update_password(client, auth_token):
#     headers = {
#         "Authorization": f"Bearer {auth_token['access_token']}",
#         "X-CSRF-TOKEN": f"{auth_token['csrf_token']}",
#     }
#     data = {
#         "password": "Erfan@2613841",  # new
#         "old_password": "Erfan@261384",  # old
#     }
#     response = client.post("/user/profile/password", headers=headers, json=data)
#     print(response.get_json())
#     assert response.status_code == 201


def test_upload_image_get_request(client, auth_token):
    headers = {
        "Authorization": f"Bearer {auth_token['access_token']}",
        "X-CSRF-TOKEN": f"{auth_token['csrf_token']}",
    }
    response = client.get("/user/upload", headers=headers)
    assert response.status_code == 405
