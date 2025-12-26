# app/shipments/routes.py
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, date, time
from app.models import ShipmentCreate
from app.db import shipments_coll
from app.auth.deps import get_current_user

router = APIRouter(prefix="/shipments", tags=["Shipments"])


@router.post("/")
async def create_shipment(payload: ShipmentCreate, current_user=Depends(get_current_user)):
    shipment = payload.dict()
    
    if shipment.get("expected_delivery_date"):
        shipment["expected_delivery_date"] = datetime.combine(
            shipment["expected_delivery_date"],
            datetime.min.time()
        )
    shipment["created_by"] = current_user["email"]
    shipment["role"] = current_user["role"]
    shipment["created_at"] = datetime.utcnow()

    result = await shipments_coll.insert_one(shipment)
    shipment["_id"] = str(result.inserted_id)

    return shipment


@router.get("/")
async def list_shipments(current_user=Depends(get_current_user)):
    query = {}

    # normal users → only their shipments
    if current_user["role"] != "admin":
        query["created_by"] = current_user["email"]

    shipments = []
    async for s in shipments_coll.find(query):
        s["_id"] = str(s["_id"])
        shipments.append(s)

    return shipments

@router.get("/analytics")
async def shipment_analytics(current_user=Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admins only")

    pipeline = [
        {"$group": {
            "_id": "$status",
            "count": {"$sum": 1}
        }}
    ]

    stats = {}
    async for row in shipments_coll.aggregate(pipeline):
        stats[row["_id"]] = row["count"]

    return {
        "total": sum(stats.values()),
        "by_status": stats
    }
