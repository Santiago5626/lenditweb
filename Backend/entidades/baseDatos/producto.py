from sqlalchemy import Column, Integer, String, Text, CheckConstraint
from .db import Base

class Producto(Base):
    __tablename__ = "producto"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    codigoInterno = Column(String, nullable=False, unique=True, index=True)
    codigoSena = Column(String, unique=True, index=True)
    serial = Column(String, unique=True, index=True)
    nombreProducto = Column(String, nullable=False)
    marca = Column(String)
    descripcion = Column(Text)
    estado = Column(String, nullable=False)
    idTipoProducto = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint('idTipoProducto IN (1, 2)', name='check_tipo_producto'),
    )
