from database import Base
from sqlalchemy import String, INTEGER, Column, DateTime, Boolean, Enum
from datetime import datetime
import enum

# Enum class which has different genders
class GenderEnum(enum.Enum):

    Male = "Male"
    Female = "Female"
    Other = "Other"


# Enum class which has different streams
class StreamEnum(enum.Enum):
    Commerce = "Commerce"
    Science = "Science"
    Arts = "Arts"


# Student model which has different student releted columns
class StudentModel(Base):

    __tablename__ = "student"

    id = Column(String(36), primary_key=True)
    first_name = Column(String(50), default=None)
    last_name = Column(String(50), default=None)
    email = Column(String(50), default=None)
    password = Column(String(255), default=None)
    roll_no = Column(String(10), default=None)
    gender = Column(Enum(GenderEnum))
    phone_no = Column(String(13))
    class_no = Column(INTEGER(), default=None)
    streams = Column(Enum(StreamEnum), default=None)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
