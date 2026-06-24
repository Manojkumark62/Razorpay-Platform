def test_leave_report(client):
    response = client.get("/reports/leaves")
    assert response.status_code == 200