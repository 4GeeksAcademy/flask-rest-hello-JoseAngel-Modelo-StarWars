from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from typing import List

db = SQLAlchemy()

character_films = db.Table(
    "character_films",
    db.Column("character_id", ForeignKey("characters.id"), primary_key=True),
    db.Column("film_id", ForeignKey("films.id"), primary_key=True),
)

class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(),nullable=False)

    favorites = db.relationship(
        "Favorite",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }
class Planet(db.Model):
    __tablename__ = "planets"
    id: Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(120))

    characters = db.relationship("Charater", back_populates = "homeworld")
    
class Character(db.Model):
    __tablename__ = "characters"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    planet_id: Mapped [int] = mapped_column (ForeignKey("planets.id"), nullable=False)

    homeworld = db.relationship("planets", back_populates = "characters")

    films: Mapped[List["Film"]] = db.relationship(
        secondary=character_films,
        back_populates="characters",
    )

    favorites = db.relationship(
        "Favorite",
        back_populates="character",
        cascade="all, delete-orphan",
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "planet_id": self.planet_id
        }

class Film(db.Model):
    __tablename__ = "films"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), unique=True)

    characters: Mapped[List["Character"]] = db.relationship(
        secondary=character_films,
        back_populates="films",
    )
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title
        }

class Favorite(db.Model):
    __tablename__ = "favorites"

    user_id: Mapped[int] = mapped_column( ForeignKey("users.id"),primary_key = True)
    character_id: Mapped[int] = mapped_column (ForeignKey("characters.id"), primary_key = True)
    note: Mapped [str] = mapped_column (String(255))

    user = db.relationship("User", back_populates="favorites")
    character = db.relationship("Character", back_populates="favorites")