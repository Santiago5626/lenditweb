from pydantic import BaseModel
from datetime import date

class Usuario(BaseModel):
    nombre: str
    email: str
    password: str
    cc: str
    rol: int
    
class Login(BaseModel):
    nombre: str
    password: str
    
