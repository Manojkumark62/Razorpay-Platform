def test_attendance_report(client):
    response = client.get("/reports/attendance")
    assert response.status_code == 200