# app/admin_routes.py
from fastapi import APIRouter, Depends
from app.auth.deps import require_role
from app.db import users_coll, shipments_coll, devices_coll, device_streams_coll

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/stats", dependencies=[Depends(require_role("admin"))])
async def stats():
    users_count = await users_coll.count_documents({})
    shipments_count = await shipments_coll.count_documents({})
    devices_count = await devices_coll.count_documents({})
    streams_count = await device_streams_coll.count_documents({})

    return {
        "users_count": users_count,
        "shipments_count": shipments_count,
        "devices_count": devices_count,
        "device_streams_count": streams_count
    }
