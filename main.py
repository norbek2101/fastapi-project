from fastapi import FastAPI, status, Depends, HTTPException
import models
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
import auth
from auth import CreateUserRequest, get_current_user

app = FastAPI()
app.include_router(auth.router)

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[Session, Depends(get_current_user)]


@app.get("/users/", status_code=status.HTTP_200_OK, tags=["users"])
async def get_users_list(user: user_dependency, db: db_dependency):
    """ To show all users list """

    users = db.query(models.User).all()

    return users


@app.get("/user/", status_code=status.HTTP_200_OK, tags=["users"])
async def get_current_user_info(user: user_dependency, db: db_dependency):
    """ To show authenticated user or Current user"""

    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return {"User": user}


@app.get("/user/{user_id}", status_code=status.HTTP_200_OK, tags=["users"])
async def get_user_info(user: user_dependency, user_id: int, db: db_dependency):
    """ To show  user info with given id """

    user_by_id = db.query(models.User).filter(models.User.id == user_id).first()

    if not user_by_id:
        raise HTTPException(status_code=401, detail=f"User not found with given id: {user_id}")

    return user_by_id


@app.put("/user/{user_id}", status_code=status.HTTP_200_OK, tags=["users"])
async def update_user_info(user_dep: user_dependency,  user_res:CreateUserRequest, user_id: int, db: db_dependency):
    """ To update user info with given id """

    user_by_id = db.query(models.User).filter(models.User.id == user_id).first()

    if not user_by_id:
        raise HTTPException(status_code=401, detail=f"User not found with given id: {user_id}")
    
    user_by_id.username = user_res.username
    db.commit()

    return {"Username":user_by_id.username, "msg": "User info updated!"}


@app.delete("/user/{user_id}", status_code=status.HTTP_200_OK, tags=["users"])
async def delet_user(user_dep: user_dependency, user_id: int, db: db_dependency):
    """ To delete selected user with given id """

    user_by_id = db.query(models.User).filter(models.User.id == user_id).first()

    if not user_by_id:
        raise HTTPException(status_code=401, detail=f"User not found with given id: {user_id}")
    
    db.delete(user_by_id)
    db.commit()

    return {"msg": "User was deleted successfully!"}
