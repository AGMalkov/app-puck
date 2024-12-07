from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated

from app.modules import User
from app.schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete

from slugify import slugify

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(User)).scalars().all()
    return result

@router.get("/user_id")
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")


@router.post("/create")
async def create_user(user_data: CreateUser, db: Annotated[Session, Depends(get_db)]):
    user_slug = slugify(user_data.username)
    stmt = insert(User).values(
        username=user_data.username,
        firstname=user_data.firstname,
        lastname=user_data.lastname,
        age=user_data.age,
        slug=user_slug
    )
    try:
        db.execute(stmt)
        db.commit()
        return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/update/{user_id}")
async def update_user(
    user_id: int,
    user_data: UpdateUser,
    db: Annotated[Session, Depends(get_db)]
):
    try:
        stmt = select(User).where(User.id == user_id)
        user = db.scalar(stmt)

        if not user:
            raise HTTPException(status_code=404, detail="User was not found")

        db.execute(
            update(User)
            .where(User.id == user_id)
            .values(
                firstname=user_data.firstname,
                lastname=user_data.lastname,
                age=user_data.age
            )
        )
        db.commit()
        return {"status_code": 200, "message": "User update is successful!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")



@router.delete("/delete/{user_id}")
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    stmt = delete(User).where(User.id == user_id)
    result = db.execute(stmt)
    db.commit()
    if result.rowcount:
        return {"status_code": status.HTTP_200_OK, "transaction": "User deletion is successful!"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")