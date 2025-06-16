from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.core.database.db import SessionLocal
from app.core.database.solicitud import Solicitud
from app.core.database.producto_solicitud import ProductoSolicitud
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ProductoSolicitudCreate(BaseModel):
    PRODUCTO_ID: int
    SOLICITUD_ID: int

class SolicitudCreate(BaseModel):
    IDENTIFICACION: str
    FECHA_REGISTRO: str
    ESTADO: Optional[str] = 'pendiente'

class SolicitudUpdate(BaseModel):
    ESTADO: str

@router.post("/crear")
async def crear_solicitud(solicitud: SolicitudCreate, db: Session = Depends(get_db)):
    try:
        nueva_solicitud = Solicitud(
            IDENTIFICACION=solicitud.IDENTIFICACION,
            FECHA_REGISTRO=datetime.strptime(solicitud.FECHA_REGISTRO, '%Y-%m-%d').date(),
            ESTADO=solicitud.ESTADO
        )
        
        db.add(nueva_solicitud)
        db.commit()
        db.refresh(nueva_solicitud)
        return nueva_solicitud

    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"detail": f"Error al crear solicitud: {str(e)}"})

@router.post("/agregar-producto")
async def agregar_producto_solicitud(producto_solicitud: ProductoSolicitudCreate, db: Session = Depends(get_db)):
    try:
        nuevo_producto_solicitud = ProductoSolicitud(
            PRODUCTO_ID=producto_solicitud.PRODUCTO_ID,
            SOLICITUD_ID=producto_solicitud.SOLICITUD_ID
        )
        
        db.add(nuevo_producto_solicitud)
        db.commit()
        db.refresh(nuevo_producto_solicitud)
        return nuevo_producto_solicitud

    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"detail": f"Error al agregar producto a solicitud: {str(e)}"})

@router.get("/obtener")
async def obtener_solicitudes(db: Session = Depends(get_db)):
    try:
        solicitudes = db.query(Solicitud).all()
        # Si no hay solicitudes, devolver lista vacía en lugar de 404
        if not solicitudes:
            return []
        
        # Convertir fechas a formato ISO para JSON
        result = []
        for solicitud in solicitudes:
            solicitud_dict = {
                "IDSOLICITUD": solicitud.IDSOLICITUD,
                "IDENTIFICACION": solicitud.IDENTIFICACION,
                "FECHA_REGISTRO": solicitud.FECHA_REGISTRO.isoformat() if solicitud.FECHA_REGISTRO else None,
                "ESTADO": solicitud.ESTADO
            }
            result.append(solicitud_dict)
        
        return result
    except Exception as e:
        print(f"Error en obtener_solicitudes: {e}")
        return JSONResponse(status_code=500, content={"detail": f"Error al obtener solicitudes: {str(e)}"})

@router.get("/buscar/{solicitud_id}")
async def buscar_solicitud(solicitud_id: int, db: Session = Depends(get_db)):
    solicitud = db.query(Solicitud).filter(Solicitud.IDSOLICITUD == solicitud_id).first()
    if not solicitud:
        return JSONResponse(status_code=404, content={"detail": "Solicitud no encontrada"})
    
    productos = db.query(ProductoSolicitud).filter(ProductoSolicitud.SOLICITUD_ID == solicitud_id).all()
    
    return {
        "solicitud": solicitud,
        "productos": productos
    }

@router.put("/actualizar-estado/{solicitud_id}")
async def actualizar_estado_solicitud(solicitud_id: int, solicitud: SolicitudUpdate, db: Session = Depends(get_db)):
    existing_solicitud = db.query(Solicitud).filter(Solicitud.IDSOLICITUD == solicitud_id).first()
    if not existing_solicitud:
        return JSONResponse(status_code=404, content={"detail": "Solicitud no encontrada"})

    try:
        existing_solicitud.ESTADO = solicitud.ESTADO
        db.commit()
        db.refresh(existing_solicitud)
        return existing_solicitud
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"detail": f"Error al actualizar estado: {str(e)}"})
