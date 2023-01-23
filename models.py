from database import Base
from sqlalchemy import String, INTEGER, Column, DateTime, Boolean, Enum
from datetime import datetime
import enum

# Enum class which has different genders
class GenderEnum(enum.Enum):

    Male = "Male"
    Female = "Female"
    Other = "Other"


# Student model which has different student releted columns
class StudentModel(Base):

    __tablename__ = "student"

    id = Column(String(36), primary_key=True)
    first_name = Column(String(50), default=None)
    last_name = Column(String(50), default=None)
    email = Column(String(50), default=None)
    roll_no = Column(String(10), default=None)
    gender = Column(Enum(GenderEnum))
    class_no = Column(INTEGER(), default=None)
    stream = Column(String(20), default=None)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
