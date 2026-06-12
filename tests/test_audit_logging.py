from app.models import AuditLog


def test_successful_registration_creates_audit_log(client, db_session):
    response = client.post(
        "/auth/register",
        json={
            "email": "audit-register@example.com",
            "password": "Password123!"
        }
    )

    assert response.status_code == 201

    audit_log = (
        db_session.query(AuditLog)
        .filter(AuditLog.event_type == "USER_REGISTERED")
        .first()
    )

    assert audit_log is not None
    assert audit_log.email == "audit-register@example.com"
    assert audit_log.success is True
    assert audit_log.details == "New user account created."


def test_failed_login_creates_audit_log(client, db_session):
    user_data = {
        "email": "failed-login@example.com",
        "password": "Password123!"
    }

    client.post("/auth/register", json=user_data)

    response = client.post(
        "/auth/login",
        json={
            "email": "failed-login@example.com",
            "password": "WrongPassword123!"
        }
    )

    assert response.status_code == 401

    audit_log = (
        db_session.query(AuditLog)
        .filter(AuditLog.event_type == "LOGIN_FAILED")
        .first()
    )

    assert audit_log is not None
    assert audit_log.email == "failed-login@example.com"
    assert audit_log.success is False
    assert audit_log.details == "Login failed because password was incorrect."


def test_note_creation_creates_audit_log(client, auth_headers, db_session):
    response = client.post(
        "/notes/",
        json={
            "title": "Audit Test Note",
            "content": "This note should create an audit log."
        },
        headers=auth_headers
    )

    assert response.status_code == 201

    audit_log = (
        db_session.query(AuditLog)
        .filter(AuditLog.event_type == "NOTE_CREATED")
        .first()
    )

    assert audit_log is not None
    assert audit_log.email == "dana@example.com"
    assert audit_log.success is True
    assert "Note created with note_id=" in audit_log.details


def test_note_update_creates_audit_log(client, auth_headers, db_session):
    create_response = client.post(
        "/notes/",
        json={
            "title": "Original Title",
            "content": "Original content."
        },
        headers=auth_headers
    )

    note_id = create_response.json()["id"]

    update_response = client.put(
        f"/notes/{note_id}",
        json={
            "title": "Updated Title",
            "content": "Updated content."
        },
        headers=auth_headers
    )

    assert update_response.status_code == 200

    audit_log = (
        db_session.query(AuditLog)
        .filter(AuditLog.event_type == "NOTE_UPDATED")
        .first()
    )

    assert audit_log is not None
    assert audit_log.email == "dana@example.com"
    assert audit_log.success is True
    assert audit_log.details == f"Note updated with note_id={note_id}."


def test_note_delete_creates_audit_log(client, auth_headers, db_session):
    create_response = client.post(
        "/notes/",
        json={
            "title": "Delete Audit Note",
            "content": "This note should create a delete audit log."
        },
        headers=auth_headers
    )

    note_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/notes/{note_id}",
        headers=auth_headers
    )

    assert delete_response.status_code == 204

    audit_log = (
        db_session.query(AuditLog)
        .filter(AuditLog.event_type == "NOTE_DELETED")
        .first()
    )

    assert audit_log is not None
    assert audit_log.email == "dana@example.com"
    assert audit_log.success is True
    assert audit_log.details == f"Note deleted with note_id={note_id}."


def test_unauthorized_note_access_creates_audit_log(client, auth_headers, db_session):
    create_response = client.post(
        "/notes/",
        json={
            "title": "Dana Private Note",
            "content": "Bob should not access this."
        },
        headers=auth_headers
    )

    note_id = create_response.json()["id"]

    client.post(
        "/auth/register",
        json={
            "email": "bob-audit@example.com",
            "password": "Password123!"
        }
    )

    bob_login_response = client.post(
        "/auth/login",
        json={
            "email": "bob-audit@example.com",
            "password": "Password123!"
        }
    )

    bob_headers = {
        "Authorization": f"Bearer {bob_login_response.json()['access_token']}"
    }

    bob_read_response = client.get(
        f"/notes/{note_id}",
        headers=bob_headers
    )

    assert bob_read_response.status_code == 404

    audit_log = (
        db_session.query(AuditLog)
        .filter(AuditLog.event_type == "UNAUTHORIZED_OR_MISSING_NOTE_READ")
        .first()
    )

    assert audit_log is not None
    assert audit_log.email == "bob-audit@example.com"
    assert audit_log.success is False
    assert f"note_id={note_id}" in audit_log.details