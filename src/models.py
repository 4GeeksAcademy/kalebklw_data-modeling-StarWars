from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Column, Integer, Table, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()
favorite_planet = Table(
    "favorite_planet",
    db.Model.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key = True),
    Column("planet_id", Integer, ForeignKey("planet.id"), primary_key = True)
)

favorite_characters = Table(
    "favorite_characters",
    db.Model.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key = True),
    Column("characters_id", Integer, ForeignKey("characters.id"), primary_key = True)
)

class User(db.Model):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    favorite_planet = relationship("Planet", secondary = favorite_planet)
    favorite_characters = relationship("Characters", secondary = favorite_characters)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorite_planet": [item.serialize() for item in self.favorite_planet],
            "favorite_characters": [item.serialize() for item in self.favorite_characters]
            # do not serialize the password, its a security breach
        }


class Planet(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(40), unique=True, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }


class Characters(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }
