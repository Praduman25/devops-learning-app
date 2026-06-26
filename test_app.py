import os
os.environ["DB_HOST"] = "localhost"  # tests won't actually hit a real DB for this simple check

from app import create_app

def test_health_check():
    app = create_app()
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}

def test_home_page():
    app = create_app()
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200