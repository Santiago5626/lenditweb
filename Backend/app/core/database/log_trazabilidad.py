from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .db import Base

class LogTrazabilidad(Base):
    __tablename__ = "GS_LOG_TRAZABILIDAD"
    
    IDLOG = Column(Integer, primary_key=True, autoincrement=True)
    IDUSUARIO = Column(Integer, ForeignKey("GS_USUARIO.IDUSUARIO"), nullable=False)
    FECHA = Column(DateTime, default=func.current_timestamp())
    ACCION = Column(String(20), nullable=False)
    NOMBRE_TABLA = Column(String(50), nullable=False)
    DATOS_ANTERIORES = Column(String(4000))
    DATOS_NUEVOS = Column(String(4000))

    # Relationship
    usuario = relationship("Usuario")

    def __repr__(self):
        return f"<LogTrazabilidad(id={self.IDLOG}, usuario={self.IDUSUARIO}, accion='{self.ACCION}', tabla='{self.NOMBRE_TABLA}')>"
