from sqlalchemy.ext.declarative import declarative_base
from enum import Enum
from database import Base
from pydantic import BaseModel
from sqlalchemy import Column, String, Boolean
from sqlalchemy import Column, Enum as EnumDB

class PerfilUsuarioEnum(Enum):
    ADMIN = 1
    USER = 2

class Status(Enum):
    REJECTED = 0
    PENDING = 1
    APPROVED = 2

class UserDB(Base):
    """Classe para estabelecer o modelo da tabela na DB"""
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    email: str = Column(String(100), primary_key=True, nullable=False)
    password: str = Column(String(255), nullable=False)
    name: str = Column(String(100), nullable=False)
    userRole: PerfilUsuarioEnum = Column(EnumDB(PerfilUsuarioEnum), nullable=False)
    status: Status = Column(EnumDB(Status), nullable=False)

class UserBase (BaseModel):
    email: str
    password: str
    name: str
    userRole: PerfilUsuarioEnum
    status: Status

class UserRequest(BaseModel):
    email: str
    password: str
    name: str
    
    
class UserResponse(UserBase):
    '''...'''
    class Config:
        orm_mode = True