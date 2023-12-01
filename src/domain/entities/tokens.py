from pydantic import BaseModel

class RefreshTokens(BaseModel):
  id: int
  email: str
  refreshToken: str