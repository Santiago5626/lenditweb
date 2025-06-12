from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base

class Sancion(Base):
    __tablename__ = "GS_SANCION"
    
    IDSANCION = Column(Integer, primary_key=True, autoincrement=True)
    IDENTIFICACION = Column(String(30), ForeignKey("GS_SOLICITANTE.IDENTIFICACION"), nullable=False)

    # Relationship
    solicitante = relationship("Solicitante")

    def __repr__(self):
        return f"<Sancion(id={self.IDSANCION}, identificacion='{self.IDENTIFICACION}')>"
