from sqlalchemy import Column, Integer, String, Date
from .db import Base 


class Producto(Base):
    __tablename__ = "producto"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    marca = Column(String, unique=True, index=True)
    idTipoProducto = Column(Integer, index=True)
    estado = Column(Integer, unique=True, index=True)
    serial = Column(String, unique=True, index=True)
    codigoSena = Column(String, unique=True, index=True)



