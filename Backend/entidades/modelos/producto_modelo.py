from pydantic import BaseModel
 
class Producto(BaseModel):
    id: int
    nombre: str
    email: str
    password: set
    ccEstudiante: str
    rol: str



