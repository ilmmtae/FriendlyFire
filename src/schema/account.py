from pydantic import BaseModel, Field


class AgeResponse(BaseModel):
    age: int = Field(..., description="The calculated age")