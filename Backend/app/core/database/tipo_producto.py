from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .db import Base

class TipoProducto(Base):
    __tablename__ = "GS_TIPO_PRODUCTO"
    
    IDTIPOPRODUCTO = Column(Integer, primary_key=True)
    NOMBRE_TIPO_PRODUCTO = Column(String(60), nullable=False, unique=True)

    # Relationship with Producto
    productos = relationship("Producto", back_populates="tipo_producto")

    def __repr__(self):
        return f"<TipoProducto(id={self.IDTIPOPRODUCTO}, nombre='{self.NOMBRE_TIPO_PRODUCTO}')>"
