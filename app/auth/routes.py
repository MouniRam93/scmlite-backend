# app/auth/routes.py
from fastapi import APIRouter, HTTPException
from app.models import UserCreate, LoginRequest, Token
from app.db import users_coll
from app.auth.security import (
    get_password_hash,
    verify_password,
    create_access_token,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=Token)
async def signup(payload: UserCreate):
    # normalize email
    email = payload.email.strip().lower()

    existing = await users_coll.find_one({"email": email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed = get_password_hash(payload.password)

    user_doc = {
        "email": email,
        "hashed_password": hashed,
        "full_name": payload.full_name,
        "role": payload.role or "user",
    }

    result = await users_coll.insert_one(user_doc)

    token = create_access_token(
        {"sub": str(result.inserted_id), "email": email, "role": user_doc["role"]}
    )

    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
async def login(payload: LoginRequest):
    # normalize email same way as signup
    email = payload.email.strip().lower()
    print("LOGIN PAYLOAD:", email)  # debug

    user = await users_coll.find_one({"email": email})
    print("USER FOUND:", user)      # debug

    if not user:
        print("LOGIN: no user for this email")  # debug
        raise HTTPException(status_code=401, detail="Invalid login credentials")


    password_ok = verify_password(payload.password, user["hashed_password"])
    print("PASSWORD OK:", password_ok)          # debug

    if not password_ok:
        print("LOGIN: password mismatch")       # debug
        raise HTTPException(status_code=401, detail="Invalid login credentials")

    token = create_access_token(
        {"sub": str(user["_id"]), "email": user["email"], "role": user["role"]}
    )

    return {"access_token": token, "token_type": "bearer"}
