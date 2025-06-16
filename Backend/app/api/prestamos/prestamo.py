from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.core.database.prestamo import Prestamo
from app.core.database.db import SessionLocal
from app.api.prestamos.prestamo_validacion import validar_prestamo, PrestamoValidacionError
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/obtener")
async def obtenerPrestamos(db: Session = Depends(get_db)):
    try:
        from app.core.database.solicitud import Solicitud
        from app.core.database.producto_solicitud import ProductoSolicitud
        
        prestamos = db.query(Prestamo).all()

        # Si no hay préstamos, devolver lista vacía en lugar de 404
        if not prestamos:
            return []
        
        # Cargar las relaciones manualmente
        result = []
        for prestamo in prestamos:
            try:
                solicitud = db.query(Solicitud).filter(Solicitud.IDSOLICITUD == prestamo.IDSOLICITUD).first()
                productos_solicitud = db.query(ProductoSolicitud).filter(ProductoSolicitud.SOLICITUD_ID == prestamo.IDSOLICITUD).all()
                
                prestamo_dict = {
                    "IDPRESTAMO": prestamo.IDPRESTAMO,
                    "IDSOLICITUD": prestamo.IDSOLICITUD,
                    "FECHA_REGISTRO": prestamo.FECHA_REGISTRO.isoformat() if prestamo.FECHA_REGISTRO else None,
                    "FECHA_LIMITE": prestamo.FECHA_LIMITE.isoformat() if prestamo.FECHA_LIMITE else None,
                    "FECHA_PROLONGACION": prestamo.FECHA_PROLONGACION.isoformat() if prestamo.FECHA_PROLONGACION else None,
                    "solicitud": {
                        "IDSOLICITUD": solicitud.IDSOLICITUD if solicitud else None,
                        "IDENTIFICACION": solicitud.IDENTIFICACION if solicitud else None,
                        "FECHA_REGISTRO": solicitud.FECHA_REGISTRO.isoformat() if solicitud and solicitud.FECHA_REGISTRO else None,
                        "ESTADO": solicitud.ESTADO if solicitud else None,
                        "productos_solicitud": [
                            {
                                "PRODUCTO_ID": ps.PRODUCTO_ID,
                                "SOLICITUD_ID": ps.SOLICITUD_ID
                            } for ps in productos_solicitud
                        ]
                    }
                }
                result.append(prestamo_dict)
            except Exception as e:
                print(f"Error procesando préstamo {prestamo.IDPRESTAMO}: {e}")
                continue
        
        return result
    except Exception as e:
        print(f"Error en obtenerPrestamos: {e}")
        return JSONResponse(status_code=500, content={"detail": f"Error al obtener préstamos: {str(e)}"})

class PrestamoCreate(BaseModel):
    IDSOLICITUD: int
    FECHA_REGISTRO: str
    FECHA_LIMITE: str

class ActualizarEstado(BaseModel):
    IDPRESTAMO: int
    ESTADO: int

class BuscarPrestamo(BaseModel):
    IDPRESTAMO: int

@router.post("/crear")
async def crear_prestamo(prestamo: PrestamoCreate, db: Session = Depends(get_db)):
    try:
        nuevo_prestamo = Prestamo(
            IDSOLICITUD=prestamo.IDSOLICITUD,
            FECHA_REGISTRO=datetime.strptime(prestamo.FECHA_REGISTRO, '%Y-%m-%d').date(),
            FECHA_LIMITE=datetime.strptime(prestamo.FECHA_LIMITE, '%Y-%m-%d').date(),
            FECHA_PROLONGACION=None
        )
        
        db.add(nuevo_prestamo)
        db.commit()
        db.refresh(nuevo_prestamo)
        return nuevo_prestamo

    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"detail": f"Error al crear préstamo: {str(e)}"})

@router.put("/actualizarEstado")
async def actualizar_estado_prestamo(prestamo: ActualizarEstado, db: Session = Depends(get_db)):
    from app.core.database.solicitud import Solicitud
    
    # Buscar el préstamo por su id
    existing_prestamo = db.query(Prestamo).filter(Prestamo.IDPRESTAMO == prestamo.IDPRESTAMO).first()

    if existing_prestamo:
        # Mapear estados numéricos a strings
        estado_map = {
            1: 'pendiente',
            2: 'aprobado',
            3: 'rechazado',
            4: 'finalizado'
        }
        
        nuevo_estado = estado_map.get(prestamo.ESTADO)
        if not nuevo_estado:
            return JSONResponse(status_code=400, content={"detail": "Estado inválido"})

        # Actualizar el estado de la solicitud asociada
        solicitud = db.query(Solicitud).filter(Solicitud.IDSOLICITUD == existing_prestamo.IDSOLICITUD).first()
        if solicitud:
            solicitud.ESTADO = nuevo_estado
            db.commit()
            return JSONResponse(status_code=200, content={"detail": "Estado actualizado"})
        else:
            return JSONResponse(status_code=404, content={"detail": "Solicitud asociada no encontrada"})
    else:
        return JSONResponse(status_code=404, content={"detail": "Préstamo No Encontrado"})

@router.delete("/eliminar")
async def eliminar_prestamo(prestamo: BuscarPrestamo, db: Session = Depends(get_db)):
    existing_prestamo = db.query(Prestamo).filter(Prestamo.IDPRESTAMO == prestamo.IDPRESTAMO).first()
    if existing_prestamo:
        try:
            db.query(Prestamo).filter(Prestamo.IDPRESTAMO == prestamo.IDPRESTAMO).delete()
            db.commit()
            return JSONResponse(status_code=200, content={"detail": "Préstamo Eliminado"})
        except Exception as e:
            db.rollback()
            return JSONResponse(status_code=500, content={"detail": f"Error al eliminar: {str(e)}"})

    return JSONResponse(status_code=404, content={"detail": "Préstamo No Existe"})

from datetime import datetime, timedelta
from pydantic import BaseModel

class ProlongacionRequest(BaseModel):
    dias: int

@router.put("/{id_prestamo}/prolongar")
async def prolongar_prestamo(id_prestamo: int, datos: ProlongacionRequest, db: Session = Depends(get_db)):
    """
    Prolongar un préstamo extendiendo su fecha límite
    """
    try:
        from app.core.database.solicitud import Solicitud
        from app.core.database.solicitante import Solicitante
        
        # Buscar el préstamo por su ID
        prestamo = db.query(Prestamo).filter(Prestamo.IDPRESTAMO == id_prestamo).first()
        
        if not prestamo:
            return JSONResponse(status_code=404, content={"detail": "Préstamo no encontrado"})

        if prestamo.FECHA_PROLONGACION:
            return JSONResponse(status_code=400, content={"detail": "El préstamo ya ha sido prolongado"})
        
        # Buscar la solicitud asociada
        solicitud = db.query(Solicitud).filter(Solicitud.IDSOLICITUD == prestamo.IDSOLICITUD).first()
        
        if not solicitud:
            return JSONResponse(status_code=404, content={"detail": "Solicitud asociada no encontrada"})
        
        # Verificar que el préstamo esté activo
        if solicitud.ESTADO not in ['pendiente', 'aprobado']:
            return JSONResponse(status_code=400, content={"detail": "El préstamo no está activo y no puede ser prolongado"})

        # Obtener el solicitante
        solicitante = db.query(Solicitante).filter(Solicitante.IDENTIFICACION == solicitud.IDENTIFICACION).first()
        if not solicitante:
            return JSONResponse(status_code=404, content={"detail": "Solicitante no encontrado"})

        # Validar días según tipo de solicitante
        if solicitante.ROL.lower() == 'aprendiz' and datos.dias > 1:
            return JSONResponse(status_code=400, content={"detail": "Los aprendices solo pueden prolongar por 1 día"})

        if datos.dias <= 0 or datos.dias > 30:
            return JSONResponse(status_code=400, content={"detail": "Los días de prolongación deben estar entre 1 y 30"})
        
        # Calcular nueva fecha límite
        fecha_limite_dt = datetime.combine(prestamo.FECHA_LIMITE, datetime.min.time())
        nueva_fecha_limite = fecha_limite_dt + timedelta(days=datos.dias)
        prestamo.FECHA_LIMITE = nueva_fecha_limite.date()
        prestamo.FECHA_PROLONGACION = datetime.now()
        
        # Guardar los cambios
        db.commit()
        
        return JSONResponse(status_code=200, content={
            "detail": f"Préstamo prolongado por {datos.dias} días",
            "prestamo_id": id_prestamo,
            "nueva_fecha_limite": prestamo.FECHA_LIMITE.isoformat()
        })
        
    except Exception as e:
        db.rollback()
        print(f"Error al prolongar préstamo: {e}")
        return JSONResponse(status_code=500, content={"detail": f"Error al prolongar préstamo: {str(e)}"})

@router.put("/{id_prestamo}/devolver")
async def devolver_prestamo(id_prestamo: int, db: Session = Depends(get_db)):
    """
    Devolver un préstamo cambiando el estado de la solicitud asociada a 'finalizado'
    """
    try:
        from app.core.database.solicitud import Solicitud
        
        # Buscar el préstamo por su ID
        prestamo = db.query(Prestamo).filter(Prestamo.IDPRESTAMO == id_prestamo).first()
        
        if not prestamo:
            return JSONResponse(status_code=404, content={"detail": "Préstamo no encontrado"})
        
        # Buscar la solicitud asociada
        solicitud = db.query(Solicitud).filter(Solicitud.IDSOLICITUD == prestamo.IDSOLICITUD).first()
        
        if not solicitud:
            return JSONResponse(status_code=404, content={"detail": "Solicitud asociada no encontrada"})
        
        # Verificar que el préstamo esté activo (pendiente o aprobado)
        if solicitud.ESTADO not in ['pendiente', 'aprobado']:
            return JSONResponse(status_code=400, content={"detail": "El préstamo no está activo y no puede ser devuelto"})
        
        # Cambiar el estado a finalizado
        solicitud.ESTADO = 'finalizado'
        
        # Guardar los cambios
        db.commit()
        
        return JSONResponse(status_code=200, content={
            "detail": "Préstamo devuelto exitosamente",
            "prestamo_id": id_prestamo,
            "solicitud_id": prestamo.IDSOLICITUD,
            "nuevo_estado": "finalizado"
        })
        
    except Exception as e:
        db.rollback()
        print(f"Error al devolver préstamo: {e}")
        return JSONResponse(status_code=500, content={"detail": f"Error al devolver préstamo: {str(e)}"})

@router.get("/buscar")
async def buscar_prestamo(id: str = None, db: Session = Depends(get_db)):
    query = db.query(Prestamo)
    if id:
        query = query.filter(Prestamo.IDPRESTAMO == id)
    
    prestamos = query.all()

    if not prestamos:
        return JSONResponse(status_code=404, content={"detail": "No se encontraron préstamos"})
    
    return prestamos
