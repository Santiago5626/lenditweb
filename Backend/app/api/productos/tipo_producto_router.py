from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database.db import get_db
from app.schemas.tipo_producto_modelo import TipoProducto, TipoProductoCreate
from . import tipo_producto
from app.api.auth.login import verify_jwt_token

router = APIRouter()

@router.get("/", response_model=List[TipoProducto])
def get_tipos_producto_endpoint(db: Session = Depends(get_db), token: str = Depends(verify_jwt_token)):
    return tipo_producto.get_tipos_producto(db)

@router.post("/", response_model=TipoProducto)
def create_tipo_producto_endpoint(tipo_data: TipoProductoCreate, db: Session = Depends(get_db), token: str = Depends(verify_jwt_token)):
    return tipo_producto.create_tipo_producto(db=db, tipo=tipo_data)

@router.get("/init", response_model=bool)
def init_tipos_producto_endpoint(db: Session = Depends(get_db), token: str = Depends(verify_jwt_token)):
    return tipo_producto.init_tipos_producto(db)
