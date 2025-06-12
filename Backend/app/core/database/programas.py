from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from .db import Base

class Programas(Base):
    __tablename__ = "GS_PROGRAMAS"
    
    CODPROGRAMA = Column(String(20), primary_key=True)
    NOMBRE_PROGRAMA = Column(String(100), nullable=False)

    # Relationship with Ficha
    fichas = relationship("Ficha", back_populates="programa")
    
    # Relationship with Solicitante (otros roles)
    solicitantes = relationship("Solicitante", foreign_keys="Solicitante.PROGRAMA", back_populates="programa")

    def __repr__(self):
        return f"<Programas(codigo='{self.CODPROGRAMA}', nombre='{self.NOMBRE_PROGRAMA}')>"
