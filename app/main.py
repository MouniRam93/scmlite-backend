# app/main.py
from fastapi import FastAPI
from app.auth.routes import router as auth_router
from app.shipments.routes import router as shipments_router
from app.devices.routes import router as devices_router
from app.admin_routes import router as admin_router
from app.db import client


app = FastAPI(title="SCMLite API")

@app.get("/")
def root():
    return {"message": "SCMLite API is running"}

# Include routers
app.include_router(auth_router)
app.include_router(shipments_router)
app.include_router(devices_router)
app.include_router(admin_router)

@app.on_event("shutdown")
async def shutdown_db():
    client.close()
