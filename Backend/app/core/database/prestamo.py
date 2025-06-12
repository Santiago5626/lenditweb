from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base

class Prestamo(Base):
    __tablename__ = "HS_PRESTAMO"
    
    IDPRESTAMO = Column(Integer, primary_key=True, autoincrement=True)
    IDSOLICITUD = Column(Integer, ForeignKey("GS_SOLICITUD.IDSOLICITUD"))
    FECHA_REGISTRO = Column(Date)
    FECHA_LIMITE = Column(Date)
    FECHA_PROLONGACION = Column(Date)

    # Relationship
    solicitud = relationship("Solicitud", back_populates="prestamos")

    def __repr__(self):
        return f"<Prestamo(id={self.IDPRESTAMO}, solicitud={self.IDSOLICITUD}, fecha_limite='{self.FECHA_LIMITE}')>"
