# app/models.py
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, constr
from datetime import datetime, date
from typing import Dict, Any

# User Models
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str | None = "user"  # user/admin

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    recaptcha: str | None = None

# Token response
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserInDB(BaseModel):
    id: str | None = None
    email: EmailStr
    hashed_password: str
    full_name: str
    role: str = "user"
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Shipment
class ShipmentCreate(BaseModel):
    # Numeric – fixed length
    shipment_id: constr(pattern=r"^\d{6}$")
    container_number: constr(pattern=r"^\d{7,10}$")

    # Route split
    route_from: str
    route_to: str

    # Logistics details
    goods_type: str
    device: str

    expected_delivery_date: date

    # Numeric – different lengths
    po_number: constr(pattern=r"^\d{5}$")
    delivery_number: constr(pattern=r"^\d{8}$")
    batch_id: constr(pattern=r"^\d{4}$")

    # Alphanumeric
    ndc_number: constr(pattern=r"^[A-Za-z0-9]{6,10}$")
    serial_number: constr(pattern=r"^[A-Za-z0-9]{8,12}$")

    description: constr(min_length=10, max_length=100)

    status: Optional[str] = "created"


# Device
class DeviceCreate(BaseModel):
    device_id: str
    shipment_id: Optional[str]
    device_type: Optional[str]
    metadata: Optional[Dict[str, Any]] = {}

    