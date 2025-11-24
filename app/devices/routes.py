# app/devices/routes.py
from fastapi import APIRouter, Depends
from app.models import DeviceCreate
from app.db import devices_coll, device_streams_coll
from app.auth.deps import get_current_user

router = APIRouter(prefix="/devices", tags=["Devices"])


@router.post("/")
async def register_device(payload: DeviceCreate, current_user=Depends(get_current_user)):
    doc = payload.dict()
    await devices_coll.insert_one(doc)
    return {"message": "Device registered"}


@router.post("/{device_id}/stream")
async def push_data(device_id: str, payload: dict, current_user=Depends(get_current_user)):
    payload["device_id"] = device_id
    await device_streams_coll.insert_one(payload)
    return {"message": "Stream data saved"}
