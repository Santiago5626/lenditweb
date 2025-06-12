from sqlalchemy import Column, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base

class Solicitante(Base):
    __tablename__ = "GS_SOLICITANTE"
    
    IDENTIFICACION = Column(String(30), primary_key=True)
    PRIMER_NOMBRE = Column(String(50), nullable=False)
    SEGUNDO_NOMBRE = Column(String(50), nullable=True)
    PRIMER_APELLIDO = Column(String(50), nullable=False)
    SEGUNDO_APELLIDO = Column(String(50), nullable=True)
    CORREO = Column(String(60), nullable=True)
    TELEFONO = Column(String(20), nullable=True)
    ROL = Column(Enum('aprendiz', 'contratista', 'funcionario', 'instructor', name='rol_enum'), nullable=False)
    
    # Para aprendices: referencia a ficha (que a su vez tiene el programa)
    FICHA = Column(String(20), ForeignKey("GS_FICHA.CODFICHA"), nullable=True)
    
    # Para otros roles: referencia directa al programa
    PROGRAMA = Column(String(20), ForeignKey("GS_PROGRAMAS.CODPROGRAMA"), nullable=True)
    
    ESTADO = Column(Enum('apto', 'no apto', name='estado_enum'), nullable=False, default='apto')

    # Relationships
    ficha = relationship("Ficha", back_populates="solicitantes", foreign_keys=[FICHA])
    programa = relationship("Programas", back_populates="solicitantes", foreign_keys=[PROGRAMA])

    def __repr__(self):
        return f"<Solicitante(IDENTIFICACION='{self.IDENTIFICACION}', nombre='{self.PRIMER_NOMBRE} {self.PRIMER_APELLIDO}')>"
