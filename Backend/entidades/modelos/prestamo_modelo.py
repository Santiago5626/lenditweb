from pydantic import BaseModel
from datetime import date

class Prestamo(BaseModel):
    ccEstudiante: str
    idProducto: int
    fechaFinal: date


class ActualizarEstado(BaseModel):
    id:int
    estado:int 

class buscar(BaseModel):
    id:int