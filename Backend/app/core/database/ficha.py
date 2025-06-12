from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base

class Ficha(Base):
    __tablename__ = "GS_FICHA"
    
    CODFICHA = Column(String(20), primary_key=True)
    CODPROGRAMA = Column(String(20), ForeignKey("GS_PROGRAMAS.CODPROGRAMA"))
    FECHA_INICIO = Column(Date)
    FECHA_FIN = Column(Date)

    # Relationship with Programas
    programa = relationship("Programas", back_populates="fichas")
    
    # Relationship with Solicitante (aprendices)
    solicitantes = relationship("Solicitante", foreign_keys="Solicitante.FICHA", back_populates="ficha")

    def __repr__(self):
        return f"<Ficha(codigo='{self.CODFICHA}', programa='{self.CODPROGRAMA}')>"
