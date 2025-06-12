from pydantic import BaseModel
from typing import Optional

class ProductoBase(BaseModel):
    CODIGO_INTERNO: str
    NOMBRE: str
    IDTIPOPRODUCTO: int  # 1 = equipo de cómputo, 2 = cargador, 3 = mouse, 4 = padmouse, 5 = tarjeta micro SD, 6 = guaya
    PLACA_SENA: Optional[str] = None
    SERIAL: Optional[str] = None
    MARCA: Optional[str] = None
    ESTADO: str
    OBSERVACIONES: Optional[str] = None

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    IDPRODUCTO: int

    class Config:
        from_attributes = True
