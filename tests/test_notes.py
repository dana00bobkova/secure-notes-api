def test_notes_requires_authentication(client):
    response = client.get("/notes/")

    assert response.status_code in [401, 403]


def test_create_note_success(client, auth_headers):
    response = client.post(
        "/notes/",
        json={
            "title": "Security Notes",
            "content": "Authentication verifies identity. Authorization checks access."
        },
        headers=auth_headers
    )

    assert response.status_code == 201

    body = response.json()

    assert body["title"] == "Security Notes"
    assert body["content"] == "Authentication verifies identity. Authorization checks access."
    assert "id" in body
    assert "owner_id" in body


def test_create_note_rejects_empty_title(client, auth_headers):
    response = client.post(
        "/notes/",
        json={
            "title": "",
            "content": "This should fail."
        },
        headers=auth_headers
    )

    assert response.status_code == 422


def test_create_note_rejects_empty_content(client, auth_headers):
    response = client.post(
        "/notes/",
        json={
            "title": "Bad Note",
            "content": ""
        },
        headers=auth_headers
    )

    assert response.status_code == 422


def test_list_notes_returns_current_users_notes(client, auth_headers):
    client.post(
        "/notes/",
        json={
            "title": "First Note",
            "content": "This is my first note."
        },
        headers=auth_headers
    )

    client.post(
        "/notes/",
        json={
            "title": "Second Note",
            "content": "This is my second note."
        },
        headers=auth_headers
    )

    response = client.get("/notes/", headers=auth_headers)

    assert response.status_code == 200

    notes = response.json()

    assert len(notes) == 2
    assert notes[0]["title"] == "First Note"
    assert notes[1]["title"] == "Second Note"


def test_read_note_success(client, auth_headers):
    create_response = client.post(
        "/notes/",
        json={
            "title": "Readable Note",
            "content": "This note should be readable by its owner."
        },
        headers=auth_headers
    )

    note_id = create_response.json()["id"]

    read_response = client.get(
        f"/notes/{note_id}",
        headers=auth_headers
    )

    assert read_response.status_code == 200
    assert read_response.json()["title"] == "Readable Note"


def test_update_note_success(client, auth_headers):
    create_response = client.post(
        "/notes/",
        json={
            "title": "Old Title",
            "content": "Old content."
        },
        headers=auth_headers
    )

    note_id = create_response.json()["id"]

    update_response = client.put(
        f"/notes/{note_id}",
        json={
            "title": "New Title",
            "content": "New content."
        },
        headers=auth_headers
    )

    assert update_response.status_code == 200

    body = update_response.json()

    assert body["title"] == "New Title"
    assert body["content"] == "New content."


def test_delete_note_success(client, auth_headers):
    create_response = client.post(
        "/notes/",
        json={
            "title": "Delete Me",
            "content": "This note will be deleted."
        },
        headers=auth_headers
    )

    note_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/notes/{note_id}",
        headers=auth_headers
    )

    assert delete_response.status_code == 204

    read_response = client.get(
        f"/notes/{note_id}",
        headers=auth_headers
    )

    assert read_response.status_code == 404


def test_user_cannot_read_another_users_note(client, auth_headers):
    dana_note_response = client.post(
        "/notes/",
        json={
            "title": "Dana Private Note",
            "content": "Bob should not be able to read this."
        },
        headers=auth_headers
    )

    dana_note_id = dana_note_response.json()["id"]

    client.post(
        "/auth/register",
        json={
            "email": "bob@example.com",
            "password": "Password123!"
        }
    )

    bob_login_response = client.post(
        "/auth/login",
        json={
            "email": "bob@example.com",
            "password": "Password123!"
        }
    )

    bob_headers = {
        "Authorization": f"Bearer {bob_login_response.json()['access_token']}"
    }

    bob_read_response = client.get(
        f"/notes/{dana_note_id}",
        headers=bob_headers
    )

    assert bob_read_response.status_code == 404
    assert bob_read_response.json()["detail"] == "Note not found."


def test_user_cannot_update_another_users_note(client, auth_headers):
    dana_note_response = client.post(
        "/notes/",
        json={
            "title": "Dana Private Note",
            "content": "Bob should not be able to update this."
        },
        headers=auth_headers
    )

    dana_note_id = dana_note_response.json()["id"]

    client.post(
        "/auth/register",
        json={
            "email": "bob-update@example.com",
            "password": "Password123!"
        }
    )

    bob_login_response = client.post(
        "/auth/login",
        json={
            "email": "bob-update@example.com",
            "password": "Password123!"
        }
    )

    bob_headers = {
        "Authorization": f"Bearer {bob_login_response.json()['access_token']}"
    }

    bob_update_response = client.put(
        f"/notes/{dana_note_id}",
        json={
            "title": "Bob Hacked This",
            "content": "This should not work."
        },
        headers=bob_headers
    )

    assert bob_update_response.status_code == 404
    assert bob_update_response.json()["detail"] == "Note not found."


def test_user_cannot_delete_another_users_note(client, auth_headers):
    dana_note_response = client.post(
        "/notes/",
        json={
            "title": "Dana Private Note",
            "content": "Bob should not be able to delete this."
        },
        headers=auth_headers
    )

    dana_note_id = dana_note_response.json()["id"]

    client.post(
        "/auth/register",
        json={
            "email": "bob-delete@example.com",
            "password": "Password123!"
        }
    )

    bob_login_response = client.post(
        "/auth/login",
        json={
            "email": "bob-delete@example.com",
            "password": "Password123!"
        }
    )

    bob_headers = {
        "Authorization": f"Bearer {bob_login_response.json()['access_token']}"
    }

    bob_delete_response = client.delete(
        f"/notes/{dana_note_id}",
        headers=bob_headers
    )

    assert bob_delete_response.status_code == 404
    assert bob_delete_response.json()["detail"] == "Note not found."