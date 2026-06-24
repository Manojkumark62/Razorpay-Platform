def test_get_employees(client):
    response = client.get("/employees")
    assert response.status_code == 200

def test_create_employee(client, auth_token):
    response = client.post("/employees", headers={"Authorization":f"Bearer {auth_token}"},
        json={
            "first_name":"John",
            "last_name":"Doe",
            "email":"john@test.com",
            "phone":"9999999999"})
    assert response.status_code in [200, 201]