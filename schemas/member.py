from datetime import datetime

from pydantic import BaseModel


class MemberCreate(BaseModel):
    name: str
    email: str
    phone: str | None = None


class MemberUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None


class MemberResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str | None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
