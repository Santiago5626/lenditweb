from pydantic import BaseModel
 
class Estudiante(BaseModel):
    cc: str
    nombre: str
    apellido: str
    email: str

class Eliminar(BaseModel):
    cc:str

