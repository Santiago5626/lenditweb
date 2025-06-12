from sqlalchemy import Column, Integer, String
from .db import Base

class Usuario(Base):
    __tablename__ = "GS_USUARIO"

    IDUSUARIO = Column(Integer, primary_key=True, autoincrement=True)
    NOMBRE_USUARIO = Column(String(255), unique=True, nullable=False)
    EMAIL = Column(String(255), unique=True, nullable=False)
    PASSWORD = Column(String(255), nullable=False)
    CC = Column(String(30), unique=True, nullable=False)
    ROL = Column(String(50), nullable=False)
    ESTADO = Column(String(50), nullable=False)

    def __repr__(self):
        return f"<Usuario(nombre='{self.NOMBRE_USUARIO}', email='{self.EMAIL}', rol='{self.ROL}')>"
