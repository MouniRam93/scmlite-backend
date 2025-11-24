# SCMLite Backend (FastAPI + MongoDB)

Backend service for the SCMLite demo project.

Implements:

- User signup & login
- JWT-based authentication
- Role Based Access Control (RBAC) with `admin` and `user` roles
- Shipments APIs
- Devices & device data stream APIs
- MongoDB persistence

---

## Tech Stack

- Python 3.x
- FastAPI
- MongoDB (local: `mongodb://localhost:27017`)
- Motor (async MongoDB driver)
- JWT via `python-jose`
- Password hashing via `passlib` (`pbkdf2_sha256`)
- Tested with Swagger UI and Postman

---

## Project Structure

```text
scmlite-backend/
  .venv/                 # virtualenv (not committed)
  app/
    __init__.py
    main.py              # FastAPI app, router includes
    db.py                # MongoDB connection & collections
    models.py            # Pydantic models (User, Shipment, Device, Streams)
    crud.py              # Data access helper functions
    utils.py             # JWT / security helpers
    auth/
      routes.py          # /auth/signup, /auth/login
      security.py        # password hashing, token creation
      deps.py            # get_current_user, require_role
    shipments/
      routes.py          # /shipments endpoints
    devices/
      routes.py          # /devices and /devices/{device_id}/stream
    admin_routes.py      # /admin/stats (admin-only)
  tests/                 # (placeholder)
  requirements.txt
  README.md
