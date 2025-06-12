from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base

class ProductoSolicitud(Base):
    __tablename__ = "GS_PRODUCTOSOLICITUD"
    
    IDPRODUCTOSOLICITUD = Column(Integer, primary_key=True, autoincrement=True)
    PRODUCTO_ID = Column(Integer, ForeignKey("GS_PRODUCTO.IDPRODUCTO"))
    SOLICITUD_ID = Column(Integer, ForeignKey("GS_SOLICITUD.IDSOLICITUD"))

    # Relationships
    producto = relationship("Producto")
    solicitud = relationship("Solicitud", back_populates="productos_solicitud")

    def __repr__(self):
        return f"<ProductoSolicitud(id={self.IDPRODUCTOSOLICITUD}, producto_id={self.PRODUCTO_ID}, solicitud={self.SOLICITUD_ID})>"
