import os

os.environ["DATABASE_URL"] = (
    "sqlite:///./test_pocketsmart.db"
)

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"


def test_home_page():
    response = client.get("/")

    assert response.status_code == 200

    assert "PocketSmart AI" in response.text


def test_register_and_login():

    email = (
        "test_"
        + str(os.getpid())
        + "@example.com"
    )

    response = client.post(
        "/api/register",
        json={
            "name": "Test User",
            "email": email,
            "password": "password123",
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    assert token


def test_home_planner():

    response = client.post(
        "/api/generate-home",
        json={
            "budget": 10000,
            "location": "India",
            "home_type": "Apartment",
            "rooms": 2,
            "style": "Modern",
            "priorities": [
                "lighting",
                "storage",
            ],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["planner_type"] == "home"

    assert "items" in data


def test_party_planner():

    response = client.post(
        "/api/generate-party",
        json={
            "budget": 10000,
            "location": "India",
            "occasion": "Birthday",
            "guests": 10,
            "food_preference": "Mixed",
            "venue_preference": "Home",
            "theme": "Simple",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["planner_type"] == "party"


def test_jewelry_planner():

    response = client.post(
        "/api/generate-jewelry",
        data={
            "budget": "3000",
            "occasion": "College",
            "jewelry_type": "Earrings",
            "metal": "Silver",
            "style": "Minimal",
            "outfit_color": "Blue",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["planner_type"] == "jewelry"