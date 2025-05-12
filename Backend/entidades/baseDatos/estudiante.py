from sqlalchemy import Column, Integer, String, Date
from .db import Base 


class Estudiante(Base):
    __tablename__ = "estudiante"
    
    cc = Column(String, primary_key=True, index=True)
    nombre = Column(String, index=True)
    apellido = Column(String, index=True)
    email = Column(String, index=True)
    

