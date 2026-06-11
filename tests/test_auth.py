def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_register_user_success(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "alice@example.com",
            "password": "Password123!"
        }
    )

    assert response.status_code == 201

    body = response.json()

    assert body["email"] == "alice@example.com"
    assert body["role"] == "user"
    assert "id" in body

    assert "password" not in body
    assert "hashed_password" not in body


def test_register_rejects_short_password(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "short@example.com",
            "password": "short"
        }
    )

    assert response.status_code == 422


def test_register_rejects_invalid_email(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "not-an-email",
            "password": "Password123!"
        }
    )

    assert response.status_code == 422


def test_register_rejects_duplicate_email(client):
    user_data = {
        "email": "duplicate@example.com",
        "password": "Password123!"
    }

    first_response = client.post("/auth/register", json=user_data)
    second_response = client.post("/auth/register", json=user_data)

    assert first_response.status_code == 201
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "An account with this email already exists."


def test_login_success(client, registered_user):
    response = client.post("/auth/login", json=registered_user)

    assert response.status_code == 200

    body = response.json()

    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_login_rejects_wrong_password(client, registered_user):
    response = client.post(
        "/auth/login",
        json={
            "email": registered_user["email"],
            "password": "WrongPassword123!"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password."


def test_auth_me_returns_current_user(client, auth_headers):
    response = client.get("/auth/me", headers=auth_headers)

    assert response.status_code == 200

    body = response.json()

    assert body["email"] == "dana@example.com"
    assert body["role"] == "user"
    assert "id" in body