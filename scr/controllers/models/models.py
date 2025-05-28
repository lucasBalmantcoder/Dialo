import datetime
from typing import List
import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from scr.db import db

# Base do SQLAlchemy
Base = db.Model


# Modelo: User
class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(sa.String(100), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(sa.String(100), unique=True, nullable=False)
    
    is_confirmed = mapped_column(sa.Boolean, default=False)
    
    password_with_hash: Mapped[str] = mapped_column(sa.String(100), nullable=False)

    # Relacionamentos
    messages: Mapped[List["Message"]] = relationship("Message", back_populates="author")
    created_rooms: Mapped[List["Room"]] = relationship("Room", back_populates="creator")
    room_associations: Mapped[List["RoomUserAssociation"]] = relationship("RoomUserAssociation", back_populates="user")


    def __repr__(self) -> str:
        return f"<User {self.username}>"

# Modelo: Room
class Room(Base):
    __tablename__ = "room"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    created_id: Mapped[int] = mapped_column(sa.ForeignKey("user.id"), nullable=False)

    # Relacionamento
    creator: Mapped["User"] = relationship("User", back_populates="created_rooms")
    user_associations: Mapped[List["RoomUserAssociation"]] = relationship("RoomUserAssociation", back_populates="room")


    def __repr__(self) -> str:
        return f"<Room {self.name}>"

# Modelo: Message
class Message(Base):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    room_id: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("user.id"), nullable=False)
    message: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    created: Mapped[datetime.datetime] = mapped_column(
        sa.DateTime, server_default=sa.func.now()
    )

    # Relacionamento
    author: Mapped["User"] = relationship("User", back_populates="messages")

    def __repr__(self) -> str:
        return f"<Message {self.message[:20]}...>"
    
class RoomUserAssociation(Base):
    __tablename__ = "room_user_association"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("user.id"), nullable=False)
    room_id: Mapped[int] = mapped_column(sa.ForeignKey("room.id"), nullable=False)
    status: Mapped[str] = mapped_column(sa.String(20), default="active")

    user: Mapped["User"] = relationship("User", back_populates="room_associations")
    room: Mapped["Room"] = relationship("Room", back_populates="user_associations")