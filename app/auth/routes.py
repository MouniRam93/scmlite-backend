# app/auth/routes.py
from fastapi import APIRouter, HTTPException
from bson import ObjectId

from app.models import UserCreate, Token
from app.db import users_coll
from app.auth.security import (
    get_password_hash,
    verify_password,
    create_access_token,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=Token)
async def signup(payload: UserCreate):
    existing = await users_coll.find_one({"email": payload.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed = get_password_hash(payload.password)

    user_doc = {
        "email": payload.email,
        "hashed_password": hashed,
        "full_name": payload.full_name,
        "role": payload.role or "user",
    }

    result = await users_coll.insert_one(user_doc)

    token = create_access_token(
        {"sub": str(result.inserted_id), "email": payload.email, "role": user_doc["role"]}
    )

    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
async def login(payload: UserCreate):
    user = await users_coll.find_one({"email": payload.email})

    if not user or not verify_password(payload.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid login credentials")

    token = create_access_token(
        {"sub": str(user["_id"]), "email": user["email"], "role": user["role"]}
    )

    return {"access_token": token, "token_type": "bearer"}
