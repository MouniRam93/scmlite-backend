# app/models.py
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, Dict, Any

# User Models
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str]
    role: Optional[str] = "user"  # user/admin

class UserInDB(BaseModel):
    id: Optional[str] = None
    email: EmailStr
    hashed_password: str
    full_name: Optional[str]
    role: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Token response
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Shipment
class ShipmentCreate(BaseModel):
    shipment_id: str
    origin: str
    destination: str
    weight_kg: float
    status: str = "created"
    created_by: str

# Device
class DeviceCreate(BaseModel):
    device_id: str
    shipment_id: Optional[str]
    device_type: Optional[str]
    metadata: Optional[Dict[str, Any]] = {}
