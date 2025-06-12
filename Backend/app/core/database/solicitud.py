from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base

class Solicitud(Base):
    __tablename__ = "GS_SOLICITUD"
    
    IDSOLICITUD = Column(Integer, primary_key=True, autoincrement=True)
    IDENTIFICACION = Column(String(30), ForeignKey("GS_SOLICITANTE.IDENTIFICACION"))
    CODIGO_INTERNO = Column(String(100), ForeignKey("GS_PRODUCTO.CODIGO_INTERNO"))
    FECHA_REGISTRO = Column(Date)
    ESTADO = Column(String(20))

    # Relationships
    solicitante = relationship("Solicitante")
    producto = relationship("Producto")
    prestamos = relationship("Prestamo", back_populates="solicitud")
    productos_solicitud = relationship("ProductoSolicitud", back_populates="solicitud")

    def __repr__(self):
        return f"<Solicitud(id={self.IDSOLICITUD}, identificacion='{self.IDENTIFICACION}', estado='{self.ESTADO}')>"
