def test_index_redirects_to_login(client):
    response = client.get("/")
    assert response.status_code == 302
    assert "/auth/login" in response.headers["Location"]


def test_login_page_loads(client):
    response = client.get("/auth/login")
    assert response.status_code == 200
    assert b"Log in" in response.data


def test_register_and_login(client):
    response = client.post(
        "/auth/register",
        data={
            "name": "Test Student",
            "username": "teststudent",
            "password": "password123",
            "confirm_password": "password123",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Dashboard" in response.data
