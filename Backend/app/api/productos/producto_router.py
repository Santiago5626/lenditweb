from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.core.database.db import get_db
from app.schemas.producto_modelo import Producto, ProductoCreate
from . import producto
from app.api.auth.login import verify_jwt_token

router = APIRouter()

@router.get("/contadores")
def get_contadores_endpoint(db: Session = Depends(get_db), token: str = Depends(verify_jwt_token)):
    return producto.get_contadores(db)

@router.get("/", response_model=List[Producto])
def get_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(verify_jwt_token)):
    productos = producto.get_productos(db, skip=skip, limit=limit)
    return productos

@router.post("/", response_model=Producto)
def create_producto_endpoint(producto_data: ProductoCreate, db: Session = Depends(get_db), token: str = Depends(verify_jwt_token)):
    return producto.create_producto(db=db, producto=producto_data)

@router.get("/{codigo_interno}", response_model=Producto)
def get_producto(codigo_interno: str, db: Session = Depends(get_db), token: str = Depends(verify_jwt_token)):
    db_producto = producto.get_producto_by_codigo(db, codigo_interno=codigo_interno)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

@router.put("/{codigo_interno}", response_model=Producto)
def update_producto_endpoint(codigo_interno: str, producto_data: ProductoCreate, db: Session = Depends(get_db), token: str = Depends(verify_jwt_token)):
    return producto.update_producto(db=db, codigo_interno=codigo_interno, producto_data=producto_data.dict())

@router.delete("/{codigo_interno}")
def delete_producto_endpoint(codigo_interno: str, db: Session = Depends(get_db), token: str = Depends(verify_jwt_token)):
    return producto.delete_producto(db=db, codigo_interno=codigo_interno)

@router.post("/importar-excel")
async def importar_productos_excel(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    token: str = Depends(verify_jwt_token)
):
    return await producto.import_from_excel(db=db, file=file)
