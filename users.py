import bcrypt
from sqlalchemy import or_
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


from models import UserModel
from schemas import UserAdd, UserLogin, UserUpdate

from config import config
from utils import generate_id, now


def get_user_by_id(db: Session, user_id: str):
    db_user = db.query(UserModel).filter(UserModel.id == user_id, UserModel.is_deleted == False).first()
    return db_user


def get_user_by_email(db: Session, email: str):
    db_user = db.query(UserModel).filter(UserModel.email == email, UserModel.is_deleted == False).first()
    return db_user


def _create_password(password: str):
    password = bytes(password, "utf-8")
    password = bcrypt.hashpw(password, config["salt"])
    password = password.decode("utf-8")
    return password


def get_user_list(
    db: Session,
    start: int,
    limit: int,
    search: str,
    sort_by: str,
    order: str
):
    query  = db.query(UserModel).filter(UserModel.is_deleted == False)

    if search != "all":
        text = f"""%{search}%"""
        query = query.filter(
            or_(
              UserModel.first_name.like(text),
              UserModel.last_name.like(text),
              UserModel.email.like(text)  
            )
        )
    
    if sort_by == "first_name":
        if order == "desc":
            query = query.order_by(UserModel.first_name.desc())
        else:
            query = query.order_by(UserModel.first_name)
    
    if sort_by == "last_name":
        if order == "desc":
            query = query.order_by(UserModel.last_name.desc())
        else:
            query = query.order_by(UserModel.last_name)
    
    if sort_by == "email":
        if order == "desc":
            query = query.order_by(UserModel.email.desc())
        else:
            query = query.order_by(UserModel.email)
    
    if sort_by == "created_at":
        if order == "desc":
            query = query.order_by(UserModel.created_at.desc())
        else:
            query = query.order_by(UserModel.created_at)
    
    else:
        query = query.order_by(UserModel.created_at.desc())

    count = query.count()
    results = query.offset(start).limit(limit).all()
    
    data = {"count": count, "list": results}
    return data


def create_user(db: Session, user: UserAdd):

    db_user = get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED, detail="Email already registerd")

    id = generate_id()
    password = _create_password(user.password)
    email = user.email.lower()
    db_user = UserModel(
        id=id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=email,
        password=password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def sign_in(db: Session, user: UserLogin):
    email = user.email.lower()
    db_user = get_user_by_email(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    hashed = db_user.password
    hashed = bytes(hashed, "utf-8")
    password = bytes(user.password, "utf-8")
    if not bcrypt.checkpw(password, hashed):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return db_user


def get_user(db: Session, user_id):
    db_user = get_user_by_id(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Is Not Found")
    return db_user


def get_all_users(db: Session):
    db_user = (
        db.query(UserModel)
        .filter(
            UserModel.is_deleted == False
        )
        .all()
    )
    return db_user


def update_user(db: Session, user_id: str, user: UserUpdate):
    db_user = get_user_by_id(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Is Not Found")
    db_user.first_name = user.first_name
    db_user.last_name = user.last_name
    db_user.updated_at = now()
    db.add(db_user)
    db.commit()
    return db_user


def delete_user(db: Session, user_id: str):
    db_user = get_user_by_id(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Is Not Found")
    db_user.is_deleted = True
    db_user.updated_at = now()
    db.commit()
    return
