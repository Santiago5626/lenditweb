from sqlalchemy import Column, Integer, String, Date
from .db import Base 


class Usuario(Base):
    __tablename__ = "usuario"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, index=True)
    cc = Column(String, unique=True, index=True)
    rol = Column(String, unique=True, index=True)
    estado = Column(String, unique=True, index=True)



