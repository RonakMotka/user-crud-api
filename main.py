from typing import List
from fastapi import FastAPI, Depends, Query, Path, Response, status
from sqlalchemy.orm import Session
from database import engine
from dependencies import get_db
import models
import schemas
import users

from fastapi.security import OAuth2PasswordRequestForm

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Auth

@app.post(
    "/sign-up",
    response_model=schemas.User,
    tags=["Authentication"]
)
def create_user(
    user: schemas.UserAdd,
    db: Session = Depends(get_db),
):
    data = users.create_user(db=db, user=user)
    return data


@app.post(
    "/sign-in",
    status_code=status.HTTP_200_OK,
    response_model=schemas.User,
    tags=["Authentication"],
)
def sign_in(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = users.sign_in(db, user)
    return db_user

# End Auth

@app.get(
    "/users",
    response_model=schemas.UserList,
    tags=["User"]
)
def get_user_list(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    start: int = 0,
    limit: int = 10,
    search: str = Query("all", min_length=3, max_length=60),
    sort_by: str = Query("all", min_length=3, max_length=20),
    order: str = Query("all", min_length=3, max_length=4)
):
    user = db.get(form_data.username, None)
    data = users.get_user_list(
        db=db,
        start=start,
        limit=limit,
        search=search,
        sort_by=sort_by,
        order=order
    )
    return data


@app.get(
    "/users/all",
    response_model=List[schemas.User],
    tags=["User"]
)
def get_all_users(
    db: Session = Depends(get_db)
):
    data = users.get_all_users(db=db)
    return data


@app.get(
    "/users/{user_id}",
    response_model=schemas.User,
    tags=["User"]
)
def get_user(
    db: Session = Depends(get_db),
    user_id: str = Path(..., min_length=36, max_length=36)
):
    data = users.get_user(db=db, user_id=user_id)
    return data


@app.put(
    "/users/{user_id}",
    response_model=schemas.User,
    tags=["User"]
)
def update_user(
    user: schemas.UserUpdate,
    db: Session = Depends(get_db),
    user_id: str = Path(..., min_length=36, max_length=36)
):
    data = users.update_user(db=db, user_id=user_id, user=user)
    return data


@app.delete(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
    tags=["User"]
)
def delete_user(
    db: Session = Depends(get_db),
    user_id: str = Path(..., min_length=36, max_length=36)
):
    users.delete_user(db=db, user_id=user_id)
    return Response(status_code=status.HTTP_200_OK)