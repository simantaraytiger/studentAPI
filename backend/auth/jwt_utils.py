from typing import Any, Dict, Optional
from fastapi import HTTPException, Request
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

SECRET_KEY = "pass"
ALGORITHM = "HS256"


def jwt_checker(request: Request):
    auth_header: Optional[str] = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token format")

    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload, "...>")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token is invalid or expired")


def gen_jwt(payload: Optional[Dict[str, Any]] = None):
    expire = datetime.now(timezone.utc) + timedelta(minutes=300)
    base_payload = payload or {}
    base_payload["exp"] = expire

    token = jwt.encode(base_payload, SECRET_KEY, algorithm=ALGORITHM)
    return token
