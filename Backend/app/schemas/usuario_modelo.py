from pydantic import BaseModel
from typing import Optional

class Login(BaseModel):
    nombre: str
    password: str

class Usuario(BaseModel):
    nombre: str
    email: str
    password: str
    cc: str
    rol: str
    estado: Optional[str] = "activo"

class UsuarioResponse(BaseModel):
    nombre: str
    email: str
    cc: str
    rol: str
    estado: str

    class Config:
        from_attributes = True
