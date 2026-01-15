from app import app
def test_health_endpoint():
    client = app.test_client()
    resp = client.get("/health")
    assert resp.status == 200
    assert resp.get_json()["status"] == "ok"