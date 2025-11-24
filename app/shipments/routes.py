# app/shipments/routes.py
from fastapi import APIRouter, Depends, HTTPException
from app.models import ShipmentCreate
from app.db import shipments_coll
from app.auth.deps import get_current_user

router = APIRouter(prefix="/shipments", tags=["Shipments"])


@router.post("/")
async def create_shipment(payload: ShipmentCreate, current_user=Depends(get_current_user)):
    shipment = payload.dict()
    result = await shipments_coll.insert_one(shipment)
    shipment["_id"] = str(result.inserted_id)
    return shipment


@router.get("/")
async def list_shipments(current_user=Depends(get_current_user)):
    shipments = []
    async for s in shipments_coll.find():
        s["_id"] = str(s["_id"])
        shipments.append(s)
    return shipments
