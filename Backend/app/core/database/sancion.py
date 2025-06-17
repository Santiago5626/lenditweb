from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum, DateTime
from sqlalchemy.orm import relationship
from .db import Base

class Sancion(Base):
    __tablename__ = "GS_SANCION"
    
    IDSANCION = Column(Integer, primary_key=True, autoincrement=True)
    IDENTIFICACION = Column(String(30), ForeignKey("GS_SOLICITANTE.IDENTIFICACION"), nullable=False)
    IDPRESTAMO = Column(Integer, ForeignKey("HS_PRESTAMO.IDPRESTAMO"), nullable=False)
    FECHA_INICIO = Column(Date, nullable=False)
    FECHA_FIN = Column(Date, nullable=False)
    DIAS_SANCION = Column(Integer, nullable=False, default=3)
    MOTIVO = Column(String(255), nullable=False, default='Entrega tardía de préstamo')
    ESTADO = Column(Enum('activa', 'cumplida', 'cancelada', name='estado_sancion_enum'), nullable=False, default='activa')
    FECHA_REGISTRO = Column(DateTime, nullable=False)

    # Relationships
    solicitante = relationship("Solicitante")
    prestamo = relationship("Prestamo")

    def __repr__(self):
        return f"<Sancion(id={self.IDSANCION}, identificacion='{self.IDENTIFICACION}', estado='{self.ESTADO}')>"
