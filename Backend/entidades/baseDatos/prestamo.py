from sqlalchemy import Column, Integer, String, Date
from .db import Base 


class Prestamo(Base):
    __tablename__ = "prestamo"
    
    id = Column(Integer, primary_key=True, index=True)
    identificacion_solicitante = Column(String, index=True)
    idProducto = Column(Integer, unique=True, index=True)
    fechaFinal = Column(Date, index=True)
    estado = Column(Integer, unique=True, index=True)
    


