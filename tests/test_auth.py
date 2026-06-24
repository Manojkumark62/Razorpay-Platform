def test_register(client):
    response = client.post("/auth/register", json={"username": "testuser", "email": "test@test.com", "password": "Password@123"})
    assert response.status_code in [200, 201]

def test_login(client):
    response = client.post("/auth/login", data={"email":"test@test.com", "password":"Password@123"})
    assert response.status_code == 200


def test_login_with_email_json(client):
    response = client.post("/auth/login", json={"email":"test@test.com", "password":"Password@123"})
    assert response.status_code == 200