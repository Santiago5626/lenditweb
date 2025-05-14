from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..baseDatos.producto import Producto
from ..modelos.producto_modelo import ProductoCreate
from fastapi import HTTPException

from fastapi import HTTPException
import logging

def get_productos(db: Session, skip: int = 0, limit: int = 100):
    try:
        productos = db.query(Producto).offset(skip).limit(limit).all()
        return productos
    except Exception as e:
        logging.error(f"Error al obtener productos: {e}")
        raise HTTPException(status_code=500, detail="Error interno al obtener productos")

def get_producto_by_codigo(db: Session, codigo_interno: str):
    return db.query(Producto).filter(Producto.codigoInterno == codigo_interno).first()

def create_producto(db: Session, producto: ProductoCreate):
    try:
        db_producto = Producto(
            codigoInterno=producto.codigoInterno,
            codigoSena=producto.codigoSena,
            serial=producto.serial,
            nombreProducto=producto.nombreProducto,
            marca=producto.marca,
            descripcion=producto.descripcion,
            estado=producto.estado,
            idTipoProducto=producto.idTipoProducto
        )
        db.add(db_producto)
        db.commit()
        db.refresh(db_producto)
        return db_producto
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="El código interno, código SENA o serial ya existe")

def update_producto(db: Session, codigo_interno: str, producto_data: dict):
    db_producto = get_producto_by_codigo(db, codigo_interno)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    for key, value in producto_data.items():
        setattr(db_producto, key, value)
    
    try:
        db.commit()
        db.refresh(db_producto)
        return db_producto
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error al actualizar el producto")

def delete_producto(db: Session, codigo_interno: str):
    db_producto = get_producto_by_codigo(db, codigo_interno)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    try:
        db.delete(db_producto)
        db.commit()
        return {"message": "Producto eliminado exitosamente"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error al eliminar el producto")
