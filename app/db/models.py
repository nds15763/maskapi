from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Enum
from database import Base
import enum


class FuelType(str, enum.Enum):
    petrol = "Petrol"
    diesel = "Diesel"


class Creative(Base):
    __tablename__ = "creative"

    creativeid = Column(Integer, primary_key=True, index=True)