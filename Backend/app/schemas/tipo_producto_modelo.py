from pydantic import BaseModel
from typing import Optional

class TipoProductoBase(BaseModel):
    NOMBRE_TIPO_PRODUCTO: str

class TipoProductoCreate(TipoProductoBase):
    pass

class TipoProducto(TipoProductoBase):
    IDTIPOPRODUCTO: int

    class Config:
        from_attributes = True
