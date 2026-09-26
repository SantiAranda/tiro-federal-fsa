from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.db import Base


class User(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    personal_data = relationship(
        "UserPersonalData",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )


class UserPersonalData(Base):
    __tablename__ = "datos_personales"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), unique=True, index=True
    )
    
    name = Column(String)
    lastname = Column(String)
    dni = Column(String, unique=True, index=True)
    birthdate = Column(Date)
    telephone = Column(String)
    domicile = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="personal_data")
