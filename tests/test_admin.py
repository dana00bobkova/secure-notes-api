from app.auth.security import hash_password
from app.models import User


def create_admin_user(db_session):
    admin_user = User(
        email="admin@example.com",
        hashed_password=hash_password("Password123!"),
        role="admin"
    )

    db_session.add(admin_user)
    db_session.commit()
    db_session.refresh(admin_user)

    return admin_user


def login_as_admin(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "admin@example.com",
            "password": "Password123!"
        }
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def test_regular_user_cannot_view_audit_logs(client, auth_headers):
    response = client.get(
        "/admin/audit-logs",
        headers=auth_headers
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required."


def test_admin_can_view_audit_logs(client, db_session):
    create_admin_user(db_session)
    admin_headers = login_as_admin(client)

    response = client.get(
        "/admin/audit-logs",
        headers=admin_headers
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_regular_user_cannot_list_users(client, auth_headers):
    response = client.get(
        "/admin/users",
        headers=auth_headers
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required."


def test_admin_can_list_users(client, db_session):
    create_admin_user(db_session)
    admin_headers = login_as_admin(client)

    response = client.get(
        "/admin/users",
        headers=admin_headers
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_admin_can_view_system_health(client, db_session):
    create_admin_user(db_session)
    admin_headers = login_as_admin(client)

    response = client.get(
        "/admin/system-health",
        headers=admin_headers
    )

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "ok"
    assert body["database"] == "connected"
    assert "users_total" in body
    assert "users_active" in body
    assert "notes_total" in body
    assert "audit_logs_total" in body


def test_regular_user_cannot_view_admin_system_health(client, auth_headers):
    response = client.get(
        "/admin/system-health",
        headers=auth_headers
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required."


def test_admin_can_disable_user(client, db_session):
    create_admin_user(db_session)
    admin_headers = login_as_admin(client)

    user_response = client.post(
        "/auth/register",
        json={
            "email": "disable-me@example.com",
            "password": "Password123!"
        }
    )

    assert user_response.status_code == 201

    user_id = user_response.json()["id"]

    disable_response = client.patch(
        f"/admin/users/{user_id}/disable",
        headers=admin_headers
    )

    assert disable_response.status_code == 200

    body = disable_response.json()

    assert body["id"] == user_id
    assert body["email"] == "disable-me@example.com"
    assert body["is_active"] is False


def test_disabled_user_cannot_login(client, db_session):
    create_admin_user(db_session)
    admin_headers = login_as_admin(client)

    user_response = client.post(
        "/auth/register",
        json={
            "email": "disabled-login@example.com",
            "password": "Password123!"
        }
    )

    assert user_response.status_code == 201

    user_id = user_response.json()["id"]

    disable_response = client.patch(
        f"/admin/users/{user_id}/disable",
        headers=admin_headers
    )

    assert disable_response.status_code == 200

    login_response = client.post(
        "/auth/login",
        json={
            "email": "disabled-login@example.com",
            "password": "Password123!"
        }
    )

    assert login_response.status_code == 401
    assert login_response.json()["detail"] == "Invalid email or password."


def test_admin_cannot_disable_self(client, db_session):
    admin_user = create_admin_user(db_session)
    admin_headers = login_as_admin(client)

    response = client.patch(
        f"/admin/users/{admin_user.id}/disable",
        headers=admin_headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Admins cannot disable their own account."