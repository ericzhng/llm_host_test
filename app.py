
from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from typing import Annotated
import uvicorn
import uuid

from server.schemas import PredictInput, CreateKeyInput, RevokeKeyInput
from server.auth import get_user_id
from server.models import llm
from server.database import init_db, insert_api_key, user_id_exists, delete_api_key, get_user_id_by_key


app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Serve static files
app.mount("/static", StaticFiles(directory="web"), name="static")

@app.post("/create-api-key")
@limiter.limit("10/minute")
async def create_api_key(request: Request, input: CreateKeyInput):
    if user_id_exists(input.user_id):
        raise HTTPException(status_code=400, detail="User ID already has an API key")
    api_key = str(uuid.uuid4())
    insert_api_key(api_key, input.user_id)
    return {"api_key": api_key, "user_id": input.user_id}

@app.post("/revoke-api-key")
@limiter.limit("10/minute")
async def revoke_api_key(request: Request, input: RevokeKeyInput, user_id: Annotated[str, Depends(get_user_id)]):
    target_user_id = get_user_id_by_key(input.api_key)
    if not target_user_id:
        raise HTTPException(status_code=404, detail="API key not found")
    if target_user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to revoke this key")
    delete_api_key(input.api_key)
    return {"message": "API key revoked"}

@app.post("/predict")
@limiter.limit("10/minute")
async def predict(request: Request, input: PredictInput, user_id: Annotated[str, Depends(get_user_id)]):
    try:
        result = llm.generate(input.text)
        return {"response": result, "user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")

if __name__ == "__main__":
    init_db()  # Initialize database
    uvicorn.run(app, host="0.0.0.0", port=8000)
