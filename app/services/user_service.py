from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user_in: UserCreate):
    user = User(
        email=user_in.email,
        password_hash=hash_password(user_in.password),
        role=user_in.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, db_user: User, user_in: UserUpdate):
    if user_in.password:
        db_user.password_hash = hash_password(user_in.password)
    
    if user_in.role is not None:
        db_user.role = user_in.role

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, db_user: User):
    db.delete(db_user)
    db.commit()
