from pydantic import BaseModel
from datetime import date

class PrestamoBase(BaseModel):
    IDENTIFICACION_SOLICITANTE: str
    IDPRODUCTO: int
    FECHA_LIMITE: date

    class Config:
        from_attributes = True

class PrestamoCreate(PrestamoBase):
    pass

class PrestamoResponse(PrestamoBase):
    IDPRESTAMO: int
    IDSOLICITUD: int
    FECHA_REGISTRO: date
    FECHA_PROLONGACION: date | None = None

class ActualizarEstado(BaseModel):
    IDPRESTAMO: int
    ESTADO: int 

class BuscarPrestamo(BaseModel):
    IDPRESTAMO: int
