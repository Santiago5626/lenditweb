from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.core.database.db import Base

class Solicitud(Base):
    __tablename__ = "GS_SOLICITUD"
    
    IDSOLICITUD = Column(Integer, primary_key=True, index=True, autoincrement=True)
    IDENTIFICACION = Column(String(30), ForeignKey("GS_SOLICITANTE.IDENTIFICACION"), nullable=False)
    FECHA_REGISTRO = Column(DateTime, nullable=False)
    ESTADO = Column(Enum('pendiente', 'aprobado', 'rechazado', 'finalizado'), default='pendiente')

    # Relaciones
    solicitante = relationship("Solicitante", backref="solicitudes")
    prestamos = relationship("Prestamo", back_populates="solicitud")
    productos_solicitud = relationship("ProductoSolicitud", back_populates="solicitud")
