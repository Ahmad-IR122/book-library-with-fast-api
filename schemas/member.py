import datetime

from database import BaseModel

class createMember(BaseModel):
    name: str
    email: str
    password: str
    role: str
    
class updateMember(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None
    role: str | None = None

class MemberResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str | None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }