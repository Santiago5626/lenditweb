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
    telefono = Column(String, nullable=True)
    rol = Column(String, nullable=False)
    ficha = Column(String, nullable=True)
    programa = Column(String, nullable=True)

    # Actualizar restricción de CHECK para los nuevos roles
    __table_args__ = (
        CheckConstraint(
            "rol IN ('aprendiz', 'contratista', 'funcionario', 'instructor')", 
            name="check_rol"
        ),
    )
