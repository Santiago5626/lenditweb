from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.core.database.tipo_producto import TipoProducto
from app.core.database.producto import Producto
from app.schemas.tipo_producto_modelo import TipoProductoCreate
from fastapi import HTTPException
import logging

def get_tipos_producto(db: Session):
    try:
        tipos = db.query(TipoProducto).all()
        return tipos
    except Exception as e:
        logging.error(f"Error al obtener tipos de producto: {e}")
        raise HTTPException(status_code=500, detail="Error interno al obtener tipos de producto")

def get_tipo_producto_by_id(db: Session, tipo_id: int):
    return db.query(TipoProducto).filter(TipoProducto.IDTIPOPRODUCTO == tipo_id).first()

def create_tipo_producto(db: Session, tipo: TipoProductoCreate):
    try:
        db_tipo = TipoProducto(
            NOMBRE_TIPO_PRODUCTO=tipo.NOMBRE_TIPO_PRODUCTO
        )
        db.add(db_tipo)
        db.commit()
        db.refresh(db_tipo)
        return db_tipo
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="El nombre del tipo de producto ya existe")

def init_tipos_producto(db: Session):
    """Inicializar tipos de producto por defecto si no existen"""
    try:
        # Lista de tipos de producto correctos
        tipos_correctos = [
            "equipo de cómputo",  # id 1
            "cargador",           # id 2
            "mouse",             # id 3
            "padmouse",          # id 4
            "tarjeta micro SD",  # id 5
            "guaya"              # id 6
        ]
        
        # Limpiar tipos incorretos si existen
        tipos_existentes = db.query(TipoProducto).all()
        for tipo_existente in tipos_existentes:
            if tipo_existente.NOMBRE_TIPO_PRODUCTO not in tipos_correctos:
                # Solo eliminar si no hay productos asociados
                productos_asociados = db.query(Producto).filter(Producto.IDTIPOPRODUCTO == tipo_existente.IDTIPOPRODUCTO).count()
                if productos_asociados == 0:
                    db.delete(tipo_existente)
                    logging.info(f"Eliminado tipo incorrecto: {tipo_existente.NOMBRE_TIPO_PRODUCTO}")
        
        # Insertar tipos correctos si no existen
        for nombre_tipo in tipos_correctos:
            existing_tipo = db.query(TipoProducto).filter(TipoProducto.NOMBRE_TIPO_PRODUCTO == nombre_tipo).first()
            if not existing_tipo:
                nuevo_tipo = TipoProducto(NOMBRE_TIPO_PRODUCTO=nombre_tipo)
                db.add(nuevo_tipo)
                logging.info(f"Agregado tipo: {nombre_tipo}")
        
        db.commit()
        logging.info("Tipos de producto inicializados correctamente")
        return True
    except Exception as e:
        db.rollback()
        logging.error(f"Error al inicializar tipos de producto: {e}")
        return False
