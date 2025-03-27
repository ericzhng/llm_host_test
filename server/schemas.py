
from pydantic import BaseModel, Field

class PredictInput(BaseModel):
    text: str = Field(..., min_length=1, max_length=500, description="Text to process")

class CreateKeyInput(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=50, pattern="^[a-zA-Z0-9_-]+$", description="Alphanumeric user ID")

class RevokeKeyInput(BaseModel):
    api_key: str = Field(..., description="API key to revoke")
