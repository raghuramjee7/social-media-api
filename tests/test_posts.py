from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    res = client.get("/") # this gives a response object
    assert res.status_code == 404

def test_create_user():
    res = client.post("/users/", json={"email": "ramjee@ram.in",
                                       "password": "ramjee123"})
    
    assert res.status_code == 201                         

