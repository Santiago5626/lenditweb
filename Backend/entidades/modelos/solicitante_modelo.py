from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class GeneroEnum(str, Enum):
    MASCULINO = 'M'
    FEMENINO = 'F'
    OTRO = 'O'

class RolEnum(str, Enum):
    APRENDIZ = 'aprendiz'
    EMPLEADO = 'empleado'

class SolicitanteBase(BaseModel):
    identificacion: str
    primer_nombre: str
    segundo_nombre: Optional[str] = None
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    correo: EmailStr
    telefono: str
    genero: GeneroEnum
    rol: RolEnum

class SolicitanteAprendiz(SolicitanteBase):
    ficha: str
    programa: str

class SolicitanteEmpleado(SolicitanteBase):
    pass

class SolicitanteResponse(SolicitanteBase):
    ficha: Optional[str] = None
    programa: Optional[str] = None

    class Config:
        orm_mode = True

class EliminarSolicitante(BaseModel):
    identificacion: str
