from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Union
from enum import Enum

class RolEnum(str, Enum):
    APRENDIZ = 'aprendiz'
    CONTRATISTA = 'contratista'
    FUNCIONARIO = 'funcionario'
    INSTRUCTOR = 'instructor'

class SolicitanteBase(BaseModel):
    identificacion: str
    primer_nombre: str
    segundo_nombre: Optional[str] = None
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    correo: Optional[Union[EmailStr, None]] = None
    telefono: str
    rol: RolEnum

class SolicitanteAprendiz(SolicitanteBase):
    ficha: str
    programa: str

class SolicitanteResponse(SolicitanteBase):
    ficha: Optional[str] = None
    programa: Optional[str] = None

    class Config:
        from_attributes = True

class EliminarSolicitante(BaseModel):
    identificacion: str

class UpdateSolicitante(BaseModel):
    identificacion: str
    primer_nombre: str
    segundo_nombre: Optional[str] = None
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    correo: Optional[Union[EmailStr, None]] = None
    telefono: str
    rol: RolEnum
    ficha: Optional[str] = None
    programa: Optional[str] = None

class EliminarMultiplesSolicitantes(BaseModel):
    identificaciones: List[str]
