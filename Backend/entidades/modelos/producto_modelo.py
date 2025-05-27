from pydantic import BaseModel
from typing import Optional

class ProductoBase(BaseModel):
    codigoInterno: str
    codigoSena: Optional[str] = None
    serial: Optional[str] = None
    nombreProducto: str
    marca: Optional[str] = None
    descripcion: Optional[str] = None
    estado: str
    idTipoProducto: int  # 1 = Equipo, 2 = Accesorio

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: int

    class Config:
        from_attributes = True
