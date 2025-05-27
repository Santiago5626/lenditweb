from sqlalchemy import Column, Integer, String
from .db import Base

class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    cc = Column(String, unique=True, nullable=False)
    rol = Column(String, nullable=False)
    estado = Column(String, nullable=False)

    def __repr__(self):
        return f"<Usuario(nombre='{self.nombre}', email='{self.email}', rol='{self.rol}')>"
