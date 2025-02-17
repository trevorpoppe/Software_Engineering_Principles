from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional

app = FastAPI()

# In-memory database simulation
devices_db: Dict[int, dict] = {}
device_id_counter = 1

class Device(BaseModel):
    name: str
    type: str
    status: str
    room: int
    house: int
    settings: dict
    id: Optional[int] = None

@app.post("/devices", response_model=Device)
def create_device(device: Device):
    global device_id_counter
    new_device = device.model_dump()
    new_device["id"] = device_id_counter
    devices_db[device_id_counter] = new_device
    device_id_counter += 1
    return Device(**new_device)

@app.get("/devices/{id}", response_model=Device)
def read_device(id: int):
    if id not in devices_db:
        raise HTTPException(status_code=404, detail="Device not found")
    device = devices_db[id]
    return Device(**device)

@app.put("/devices/{id}", response_model=Device)
def update_device(id: int, device: Device):
    if id not in devices_db:
        raise HTTPException(status_code=404, detail="Device not found")
    updated_device = device.model_dump()
    updated_device["id"] = id
    devices_db[id] = updated_device
    return Device(**updated_device)

@app.delete("/devices/{id}")
def delete_device(id: int):
    if id not in devices_db:
        raise HTTPException(status_code=404, detail="Device not found")
    del devices_db[id]
    return {"message": "Device deleted successfully"}

@app.get("/houses/{house_id}/devices", response_model=List[Device])
def list_devices(house_id: int):
    return [Device(**device) for device in devices_db.values() if device["house"] == house_id]

@app.get("/rooms/{room_id}/devices", response_model=List[Device])
def list_devices_in_room(room_id: int):
    return [Device(**device) for device in devices_db.values() if device["room"] == room_id]
