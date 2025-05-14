from sqlalchemy import Column, String, CheckConstraint
from .db import Base

class Solicitante(Base):
    __tablename__ = "solicitante"
    
    identificacion = Column(String, primary_key=True)
    primer_nombre = Column(String, nullable=False)
    segundo_nombre = Column(String, nullable=True)
    primer_apellido = Column(String, nullable=False)
    segundo_apellido = Column(String, nullable=True)
    correo = Column(String, nullable=False, unique=True)
    telefono = Column(String, nullable=False)
    genero = Column(String(1), nullable=False)
    rol = Column(String, nullable=False)
    ficha = Column(String, nullable=True)
    programa = Column(String, nullable=True)

    # Agregar restricciones de CHECK
    __table_args__ = (
        CheckConstraint("genero IN ('M', 'F')", name="check_genero"),
        CheckConstraint("rol IN ('aprendiz', 'empleado')", name="check_rol"),
    )
