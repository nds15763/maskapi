# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import List
from sqlalchemy.orm import Session
import models

DATABASE_URL = "mysql+mysqldb://db_admin:Xxp719765843,.@host/mask_db"

class DB:

    def __init__(self):
        self.db_engine = create_engine(DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.db_engine)
        self.Base = declarative_base()

    def GetCreative(db: Session, creative_id: int):
        return db.query(models.Creative).filter(models.Creative.creativeid == creative_id).first()

    # def get_user(db: Session, user_id: int):
    #     return db.query(models.User).filter(models.User.id == user_id).first()


    # def get_user_by_email(db: Session, email: str):
    #     return db.query(models.User).filter(models.User.email == email).first()


    # def get_users(db: Session, skip: int = 0, limit: int = 100):
    #     return db.query(models.User).offset(skip).limit(limit).all()


    # def create_user(db: Session, user: schemas.UserCreate):
    #     fake_hashed_password = user.password + "notreallyhashed"
    #     db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    #     db.add(db_user)
    #     db.commit()
    #     db.refresh(db_user)
    #     return db_user


    # def get_items(db: Session, skip: int = 0, limit: int = 100):
    #     return db.query(models.Item).offset(skip).limit(limit).all()


    # def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    #     db_item = models.Item(**item.dict(), owner_id=user_id)
    #     db.add(db_item)
    #     db.commit()
    #     db.refresh(db_item)
    #     return db_item