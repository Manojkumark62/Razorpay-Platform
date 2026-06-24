def test_inventory_report(client):
    response = client.get("/reports/inventory")
    assert response.status_code == 200