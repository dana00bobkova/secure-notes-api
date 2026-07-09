def test_login_rate_limit_rejects_repeated_attempts(client):
    user_data = {
        "email": "rate-login@example.com",
        "password": "Password123!"
    }

    response = client.post("/auth/register", json=user_data)

    assert response.status_code == 201

    for _ in range(5):
        response = client.post(
            "/auth/login",
            json={
                "email": user_data["email"],
                "password": "WrongPassword123!"
            }
        )

        assert response.status_code == 401

    response = client.post(
        "/auth/login",
        json={
            "email": user_data["email"],
            "password": "WrongPassword123!"
        }
    )

    assert response.status_code == 429
    assert response.json()["detail"] == "Too many requests. Please try again later."


def test_note_creation_rate_limit_rejects_repeated_requests(client, auth_headers):
    for index in range(5):
        response = client.post(
            "/notes/",
            json={
                "title": f"Rate Limited Note {index}",
                "content": "This note creation request is part of the rate limit test."
            },
            headers=auth_headers
        )

        assert response.status_code == 201

    response = client.post(
        "/notes/",
        json={
            "title": "Too Many Notes",
            "content": "This request should be blocked by rate limiting."
        },
        headers=auth_headers
    )

    assert response.status_code == 429
    assert response.json()["detail"] == "Too many requests. Please try again later."
