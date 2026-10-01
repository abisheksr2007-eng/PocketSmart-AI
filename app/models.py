from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(120), nullable=False)

    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash = Column(String(255), nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    recommendations = relationship(
        "Recommendation",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
    )

    planner_type = Column(
        String(50),
        nullable=False,
    )

    title = Column(
        String(255),
        nullable=False,
    )

    input_json = Column(
        Text,
        nullable=False,
    )

    result_json = Column(
        Text,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="recommendations",
    )