from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

app = FastAPI()

client = TestClient(app)

def test_create_device():
    response = client.post("/devices", json={
        "name": "Smart Thermostat",
        "type": "thermostat",
        "status": "on",
        "room": 1,
        "house": 1,
        "settings": {"temperature": 72}
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Smart Thermostat"

def test_read_device():
    create_response = client.post("/devices", json={
        "name": "Smart Thermostat",
        "type": "thermostat",
        "status": "on",
        "room": 1,
        "house": 1,
        "settings": {"temperature": 72}
    })
    assert create_response.status_code == 200, f"Device creation failed: {create_response.text}"

    device_id = create_response.json()["id"]

    response = client.get(f"/devices/{device_id}")

    assert response.status_code == 200, f"Device read failed: {response.text}"
    assert response.json()["id"] == device_id

def test_update_device():
    create_response = client.post("/devices", json={
        "name": "Smart Thermostat",
        "type": "thermostat",
        "status": "on",
        "room": 1,
        "house": 1,
        "settings": {"temperature": 72}
    })
    assert create_response.status_code == 200

    device_id = create_response.json()["id"]

    update_response = client.put(f"/devices/{device_id}", json={
        "name": "Smart Thermostat",
        "type": "thermostat",
        "status": "off",
        "room": 1,
        "house": 1,
        "settings": {"temperature": 68}
    })
    assert update_response.status_code == 200, f"Device update failed: {update_response.text}"
    assert update_response.json()["status"] == "off"

def test_delete_device():
    create_response = client.post("/devices", json={
        "name": "Smart Thermostat",
        "type": "thermostat",
        "status": "on",
        "room": 1,
        "house": 1,
        "settings": {"temperature": 72}
    })
    assert create_response.status_code == 200
    device_id = create_response.json()["id"]

    response = client.delete(f"/devices/{device_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Device deleted successfully"

def test_list_devices():
    client.post("/devices", json={
        "name": "Smart Light",
        "type": "light",
        "status": "off",
        "room": 2,
        "house": 1,
        "settings": {"brightness": 80}
    })
    response = client.get("/houses/1/devices")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_list_devices_in_room():
    client.post("/devices", json={
        "name": "Smart Light",
        "type": "light",
        "status": "off",
        "room": 2,
        "house": 1,
        "settings": {"brightness": 80}
    })
    response = client.get("/rooms/2/devices")
    assert response.status_code == 200
    assert response.json()[0]["name"] == "Smart Light"
