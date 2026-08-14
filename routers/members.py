from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.member import Member
from schemas.member import MemberCreate, MemberUpdate, MemberResponse

router = APIRouter(prefix="/members", tags=["Members"])


@router.get("/get-members", response_model=list[MemberResponse])
def get_members(db: Session = Depends(get_db)):
    return db.query(Member).all()

@router.get("/get-member/{member_id}", response_model=MemberResponse)
def get_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member

@router.post("/create-member", response_model=MemberResponse, status_code=201)
def create_member(member: MemberCreate, db: Session = Depends(get_db)):
    new_member = Member(**member.model_dump())
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member

@router.put("/update-member/{member_id}", response_model=MemberResponse)
def update_member(member_id: int, member_update: MemberUpdate, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    update_data = member_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(member, key, value)
    db.commit()
    db.refresh(member)
    return member

@router.delete("/delete-member/{member_id}", status_code=204)
def delete_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    db.delete(member)
    db.commit()
    return {
      "message": "Member deleted successfully"
    }
