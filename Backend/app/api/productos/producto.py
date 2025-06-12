from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.core.database.producto import Producto
from app.schemas.producto_modelo import ProductoCreate
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
    return db.query(Producto).filter(Producto.CODIGO_INTERNO == codigo_interno).first()

def create_producto(db: Session, producto: ProductoCreate):
    try:
        # Verificar que el tipo de producto existe
        from .tipo_producto import get_tipo_producto_by_id
        tipo_producto = get_tipo_producto_by_id(db, producto.IDTIPOPRODUCTO)
        if not tipo_producto:
            raise HTTPException(status_code=400, detail="El tipo de producto no existe")

        # Validar campos únicos solo para equipo de cómputo
        if tipo_producto.NOMBRE_TIPO_PRODUCTO == "equipo de cómputo":
            # Verificar si ya existe un producto con la misma placa SENA
            placa_sena = producto.PLACA_SENA
            if placa_sena:
                existing_placa = db.query(Producto).filter(Producto.PLACA_SENA == placa_sena).first()
                if existing_placa:
                    raise HTTPException(status_code=400, detail="La placa SENA ya existe")
            
            # Verificar si ya existe un producto con el mismo serial
            serial = producto.SERIAL
            if serial:
                existing_serial = db.query(Producto).filter(Producto.SERIAL == serial).first()
                if existing_serial:
                    raise HTTPException(status_code=400, detail="El serial ya existe")

        # Verificar si ya existe un producto con el mismo código interno
        codigo_interno = producto.CODIGO_INTERNO
        existing_codigo = db.query(Producto).filter(Producto.CODIGO_INTERNO == codigo_interno).first()
        if existing_codigo:
            raise HTTPException(status_code=400, detail="El código interno ya existe")

        db_producto = Producto(
            CODIGO_INTERNO=producto.CODIGO_INTERNO,
            NOMBRE=producto.NOMBRE,
            IDTIPOPRODUCTO=producto.IDTIPOPRODUCTO,
            PLACA_SENA=producto.PLACA_SENA,
            SERIAL=producto.SERIAL,
            MARCA=producto.MARCA,
            ESTADO=producto.ESTADO,
            OBSERVACIONES=producto.OBSERVACIONES
        )
        db.add(db_producto)
        db.commit()
        db.refresh(db_producto)
        return db_producto
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error al crear el producto")

def update_producto(db: Session, codigo_interno: str, producto_data: dict):
    db_producto = get_producto_by_codigo(db, codigo_interno)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Verificar que el tipo de producto existe si se está actualizando
    tipo_producto = None
    if 'IDTIPOPRODUCTO' in producto_data:
        from .tipo_producto import get_tipo_producto_by_id
        tipo_producto = get_tipo_producto_by_id(db, producto_data['IDTIPOPRODUCTO'])
        if not tipo_producto:
            raise HTTPException(status_code=400, detail="El tipo de producto no existe")
    else:
        # Obtener el tipo actual del producto
        from .tipo_producto import get_tipo_producto_by_id
        tipo_producto = get_tipo_producto_by_id(db, db_producto.IDTIPOPRODUCTO)
    
    # Validar campos únicos solo para equipo de cómputo
    if tipo_producto and tipo_producto.NOMBRE_TIPO_PRODUCTO == "equipo de cómputo":
        # Verificar placa SENA si se está actualizando
        if 'PLACA_SENA' in producto_data and producto_data['PLACA_SENA']:
            existing_placa = db.query(Producto).filter(
                Producto.PLACA_SENA == producto_data['PLACA_SENA'],
                Producto.CODIGO_INTERNO != codigo_interno
            ).first()
            if existing_placa:
                raise HTTPException(status_code=400, detail="La placa SENA ya existe")
        
        # Verificar serial si se está actualizando
        if 'SERIAL' in producto_data and producto_data['SERIAL']:
            existing_serial = db.query(Producto).filter(
                Producto.SERIAL == producto_data['SERIAL'],
                Producto.CODIGO_INTERNO != codigo_interno
            ).first()
            if existing_serial:
                raise HTTPException(status_code=400, detail="El serial ya existe")
    
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

def get_contadores(db: Session):
    try:
        # Obtener contadores por tipo de producto
        from .tipo_producto import get_tipos_producto
        tipos_producto = get_tipos_producto(db)
        
        contadores = {}
        
        for tipo in tipos_producto:
            disponibles = db.query(Producto).filter(
                Producto.IDTIPOPRODUCTO == tipo.IDTIPOPRODUCTO,
                Producto.ESTADO == "Disponible"
            ).count()
            
            no_disponibles = db.query(Producto).filter(
                Producto.IDTIPOPRODUCTO == tipo.IDTIPOPRODUCTO,
                Producto.ESTADO != "Disponible"
            ).count()
            
            # Crear nombres de claves basados en el nombre del tipo
            nombre_key = tipo.NOMBRE_TIPO_PRODUCTO.replace(" ", "_").replace("ó", "o")
            contadores[f"{nombre_key}_disponibles"] = disponibles
            contadores[f"{nombre_key}_no_disponibles"] = no_disponibles
        
        # Mantener compatibilidad con nombres anteriores
        total_disponibles = db.query(Producto).filter(Producto.ESTADO == "Disponible").count()
        total_no_disponibles = db.query(Producto).filter(Producto.ESTADO != "Disponible").count()
        
        contadores["totalDisponibles"] = total_disponibles
        contadores["totalNoDisponibles"] = total_no_disponibles
        
        return contadores
    except Exception as e:
        logging.error(f"Error al obtener contadores: {e}")
        raise HTTPException(status_code=500, detail="Error interno al obtener contadores")
