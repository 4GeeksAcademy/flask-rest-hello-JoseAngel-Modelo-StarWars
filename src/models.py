from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from typing import List

# ✅ Buen uso de SQLAlchemy para definir modelos

# Tabla intermedia para la relación entre personajes y películas
character_films = db.Table(
    "character_films",
    db.Column("character_id", ForeignKey("characters.id"), primary_key=True),
    db.Column("film_id", ForeignKey("films.id"), primary_key=True),
)

class User(db.Model):
    __tablename__ = "users"  # 📝 Cambié el nombre de la tabla a plural para seguir la convención

    id: Mapped[int] = mapped_column(primary_key=True)  # ✅ Buen uso de Mapped
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)  # ✅ Buen uso de restricciones
    password: Mapped[str] = mapped_column(nullable=False)  # 🔧 Añadir tipo de datos para mayor claridad
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)  # ✅ Buen uso de Boolean

    favorites = db.relationship(
        "Favorite",
        back_populates="user",
        cascade="all, delete-orphan",
    )  # ✅ Buen uso de relaciones

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    __tablename__ = "planets"  # 📝 Cambié el nombre de la tabla a plural
    id: Mapped[int] = mapped_column(primary_key=True)  # ✅ Buen uso de Mapped
    name: Mapped[str] = mapped_column(String(120))  # ✅ Buen uso de Mapped

    characters = db.relationship("Character", back_populates="homeworld")  # ✅ Buen uso de relaciones
    favorites = db.relationship("Favorite", back_populates="planet")  # ✅ Buen uso de relaciones

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }
    
class Character(db.Model):
    __tablename__ = "characters"  # 📝 Cambié el nombre de la tabla a plural
    
    id: Mapped[int] = mapped_column(primary_key=True)  # ✅ Buen uso de Mapped
    name: Mapped[str] = mapped_column(String(120), unique=True)  # ✅ Buen uso de restricciones
    planet_id: Mapped[int] = mapped_column(ForeignKey("planets.id"), nullable=False)  # ✅ Buen uso de ForeignKey

    homeworld = db.relationship("Planet", back_populates="characters")  # ✅ Buen uso de relaciones

    films: Mapped[List["Film"]] = db.relationship(
        "Film",
        secondary=character_films,
        back_populates="characters",
    )  # ✅ Buen uso de relaciones

    favorites = db.relationship(
        "Favorite",
        back_populates="character",
        cascade="all, delete-orphan",
    )  # ✅ Buen uso de relaciones

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "planet_id": self.planet_id
        }

class Film(db.Model):
    __tablename__ = "films"  # 📝 Cambié el nombre de la tabla a plural
    
    id: Mapped[int] = mapped_column(primary_key=True)  # ✅ Buen uso de Mapped
    title: Mapped[str] = mapped_column(String(200), unique=True)  # ✅ Buen uso de restricciones

    characters: Mapped[List["Character"]] = db.relationship(
        "Character",
        secondary=character_films,
        back_populates="films",
    )  # ✅ Buen uso de relaciones
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title
        }

class Favorite(db.Model):
    __tablename__ = "favorites"  # 📝 Cambié el nombre de la tabla a plural

    id: Mapped[int] = mapped_column(primary_key=True)  # ✅ Buen uso de Mapped
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)  # ✅ Buen uso de ForeignKey
    
    character_id: Mapped[int] = mapped_column(ForeignKey("characters.id"), nullable=True)  # ✅ Buen uso de ForeignKey
    planet_id: Mapped[int] = mapped_column(ForeignKey("planets.id"), nullable=True)  # ✅ Buen uso de ForeignKey
    
    note: Mapped[str] = mapped_column(String(255), nullable=True)  # ✅ Buen uso de Mapped

    user = db.relationship("User", back_populates="favorites")  # ✅ Buen uso de relaciones
    character = db.relationship("Character", back_populates="favorites")  # ✅ Buen uso de relaciones
    planet = db.relationship("Planet", back_populates="favorites")  # ✅ Buen uso de relaciones

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
            "note": self.note
        }