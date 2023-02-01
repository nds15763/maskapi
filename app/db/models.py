from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Enum
# from db.database import Base
import enum


class FuelType(str, enum.Enum):
    petrol = "Petrol"
    diesel = "Diesel"


class Creative():
    __tablename__ = "creative"

    creativeID = Column(Integer, primary_key=True, index=True)
    videoID = Column(Integer)
    picID = Column(Integer)
    cc = Column(Integer)

class Video():
    __tablename__ = "video"

    videoID = Column(Integer, primary_key=True, index=True)
    #视频存储路径
    videoSrc = Column(String)
    #视频存储名称
    videoName = Column(String)