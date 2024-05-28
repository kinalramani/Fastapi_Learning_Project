from sqlalchemy import Column,String,Boolean,DateTime
from sqlalchemy.orm import relationship
from database.database import Base
from datetime import datetime
import uuid



class Employee(Base):
    __tablename__="users"
    id=Column(String(100),primary_key=True,default=str(uuid.uuid4()))
    emp_name=Column(String(100),nullable=False)
    email=Column(String(50),nullable=False)
    mobile_no=Column(String(10),nullable=False)
    position=Column(String(100),nullable=False)
    password=Column(String(100),nullable=False)
    is_deleted=Column(Boolean,default=False)
    is_active=Column(Boolean,default=True)
    created_at=Column(DateTime,default=datetime.now)
    modified_at=Column(DateTime,default=datetime.now,onupdate=datetime.now)
