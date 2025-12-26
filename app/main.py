# app/main.py
from fastapi import FastAPI
from app.auth.routes import router as auth_router
from app.shipments.routes import router as shipments_router
from app.devices.routes import router as devices_router
from app.admin_routes import router as admin_router
from app.errors import register_exception_handlers
from fastapi.middleware.cors import CORSMiddleware
from app.db import client


app = FastAPI(title="SCMLite API")

# register the global handlers right after creating the app
register_exception_handlers(app)

# Enable CORS so frontend (http://127.0.0.1:5500) can access backend (http://127.0.0.1:8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Allow all origins (frontend)
    allow_credentials=True,
    allow_methods=["*"],      # Allow all methods
    allow_headers=["*"],      # Allow all headers
)


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
