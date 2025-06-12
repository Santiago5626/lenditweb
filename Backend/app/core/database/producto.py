from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base

class Producto(Base):
    __tablename__ = "GS_PRODUCTO"
    
    IDPRODUCTO = Column(Integer, primary_key=True, autoincrement=True)
    CODIGO_INTERNO = Column(String(100), nullable=False, unique=True)
    NOMBRE = Column(String(100), nullable=False)
    IDTIPOPRODUCTO = Column(Integer, ForeignKey("GS_TIPO_PRODUCTO.IDTIPOPRODUCTO"), nullable=False)
    PLACA_SENA = Column(String(50), unique=True)
    SERIAL = Column(String(100), unique=True)
    MARCA = Column(String(60))
    ESTADO = Column(String(20), nullable=False)
    OBSERVACIONES = Column(Text)

    # Relationship
    tipo_producto = relationship("TipoProducto", back_populates="productos")

    def __repr__(self):
        return f"<Producto(id={self.IDPRODUCTO}, codigo='{self.CODIGO_INTERNO}', nombre='{self.NOMBRE}')>"
