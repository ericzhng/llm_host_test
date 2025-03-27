from fastapi import HTTPException, Depends
from fastapi.security import APIKeyHeader
from typing import Annotated

from .database import get_user_id_by_key


api_key_header = APIKeyHeader(name="X-API-Key")

async def get_user_id(api_key: Annotated[str, Depends(api_key_header)]):
    if not api_key:
        raise HTTPException(status_code=401, detail="API Key missing")
    user_id = get_user_id_by_key(api_key)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return user_id
