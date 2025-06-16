from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database.db import Base

class ProductoSolicitud(Base):
    __tablename__ = "GS_PRODUCTO_SOLICITUD"
    
    PRODUCTO_ID = Column(Integer, ForeignKey("GS_PRODUCTO.IDPRODUCTO"), primary_key=True)
    SOLICITUD_ID = Column(Integer, ForeignKey("GS_SOLICITUD.IDSOLICITUD"), primary_key=True)

    # Relaciones
    producto = relationship("Producto", back_populates="productos_solicitud")
    solicitud = relationship("Solicitud", back_populates="productos_solicitud")
