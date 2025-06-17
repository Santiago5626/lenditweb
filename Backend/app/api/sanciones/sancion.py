from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date, datetime

from app.core.database.db import get_db
from app.core.database.sancion import Sancion
from app.core.database.solicitante import Solicitante
from app.core.database.prestamo import Prestamo

router = APIRouter()

@router.get("/", response_model=List[dict])
def obtener_sanciones(db: Session = Depends(get_db)):
    """Obtener todas las sanciones con información del solicitante y préstamo"""
    try:
        sanciones = db.query(Sancion).join(
            Solicitante, Sancion.IDENTIFICACION == Solicitante.IDENTIFICACION
        ).join(
            Prestamo, Sancion.IDPRESTAMO == Prestamo.IDPRESTAMO
        ).all()
        
        resultado = []
        for sancion in sanciones:
            solicitante = sancion.solicitante
            prestamo = sancion.prestamo
            
            resultado.append({
                "IDSANCION": sancion.IDSANCION,
                "IDENTIFICACION": sancion.IDENTIFICACION,
                "IDPRESTAMO": sancion.IDPRESTAMO,
                "FECHA_INICIO": sancion.FECHA_INICIO.isoformat() if sancion.FECHA_INICIO else None,
                "FECHA_FIN": sancion.FECHA_FIN.isoformat() if sancion.FECHA_FIN else None,
                "DIAS_SANCION": sancion.DIAS_SANCION,
                "MOTIVO": sancion.MOTIVO,
                "ESTADO": sancion.ESTADO,
                "FECHA_REGISTRO": sancion.FECHA_REGISTRO.isoformat() if sancion.FECHA_REGISTRO else None,
                "solicitante": {
                    "PRIMER_NOMBRE": solicitante.PRIMER_NOMBRE,
                    "SEGUNDO_NOMBRE": solicitante.SEGUNDO_NOMBRE,
                    "PRIMER_APELLIDO": solicitante.PRIMER_APELLIDO,
                    "SEGUNDO_APELLIDO": solicitante.SEGUNDO_APELLIDO,
                    "ROL": solicitante.ROL,
                    "ESTADO": solicitante.ESTADO
                },
                "prestamo": {
                    "FECHA_REGISTRO": prestamo.FECHA_REGISTRO.isoformat() if prestamo.FECHA_REGISTRO else None,
                    "FECHA_LIMITE": prestamo.FECHA_LIMITE.isoformat() if prestamo.FECHA_LIMITE else None
                }
            })
        
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener sanciones: {str(e)}")

@router.get("/activas", response_model=List[dict])
def obtener_sanciones_activas(db: Session = Depends(get_db)):
    """Obtener solo las sanciones activas"""
    try:
        sanciones = db.query(Sancion).filter(
            Sancion.ESTADO == 'activa'
        ).join(
            Solicitante, Sancion.IDENTIFICACION == Solicitante.IDENTIFICACION
        ).all()
        
        resultado = []
        for sancion in sanciones:
            solicitante = sancion.solicitante
            
            resultado.append({
                "IDSANCION": sancion.IDSANCION,
                "IDENTIFICACION": sancion.IDENTIFICACION,
                "FECHA_INICIO": sancion.FECHA_INICIO.isoformat() if sancion.FECHA_INICIO else None,
                "FECHA_FIN": sancion.FECHA_FIN.isoformat() if sancion.FECHA_FIN else None,
                "DIAS_SANCION": sancion.DIAS_SANCION,
                "MOTIVO": sancion.MOTIVO,
                "solicitante": {
                    "PRIMER_NOMBRE": solicitante.PRIMER_NOMBRE,
                    "SEGUNDO_NOMBRE": solicitante.SEGUNDO_NOMBRE,
                    "PRIMER_APELLIDO": solicitante.PRIMER_APELLIDO,
                    "SEGUNDO_APELLIDO": solicitante.SEGUNDO_APELLIDO,
                    "ROL": solicitante.ROL
                }
            })
        
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener sanciones activas: {str(e)}")

@router.get("/solicitante/{identificacion}", response_model=List[dict])
def obtener_sanciones_solicitante(identificacion: str, db: Session = Depends(get_db)):
    """Obtener sanciones de un solicitante específico"""
    try:
        sanciones = db.query(Sancion).filter(
            Sancion.IDENTIFICACION == identificacion
        ).all()
        
        resultado = []
        for sancion in sanciones:
            resultado.append({
                "IDSANCION": sancion.IDSANCION,
                "IDPRESTAMO": sancion.IDPRESTAMO,
                "FECHA_INICIO": sancion.FECHA_INICIO.isoformat() if sancion.FECHA_INICIO else None,
                "FECHA_FIN": sancion.FECHA_FIN.isoformat() if sancion.FECHA_FIN else None,
                "DIAS_SANCION": sancion.DIAS_SANCION,
                "MOTIVO": sancion.MOTIVO,
                "ESTADO": sancion.ESTADO,
                "FECHA_REGISTRO": sancion.FECHA_REGISTRO.isoformat() if sancion.FECHA_REGISTRO else None
            })
        
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener sanciones del solicitante: {str(e)}")

@router.put("/{sancion_id}/cumplir")
def marcar_sancion_cumplida(sancion_id: int, db: Session = Depends(get_db)):
    """Marcar una sanción como cumplida y restaurar el estado del solicitante"""
    try:
        sancion = db.query(Sancion).filter(Sancion.IDSANCION == sancion_id).first()
        if not sancion:
            raise HTTPException(status_code=404, detail="Sanción no encontrada")
        
        if sancion.ESTADO != 'activa':
            raise HTTPException(status_code=400, detail="Solo se pueden cumplir sanciones activas")
        
        # Marcar sanción como cumplida
        sancion.ESTADO = 'cumplida'
        
        # Verificar si el solicitante tiene otras sanciones activas
        otras_sanciones_activas = db.query(Sancion).filter(
            Sancion.IDENTIFICACION == sancion.IDENTIFICACION,
            Sancion.ESTADO == 'activa',
            Sancion.IDSANCION != sancion_id
        ).count()
        
        # Si no tiene otras sanciones activas, restaurar estado a 'apto'
        if otras_sanciones_activas == 0:
            solicitante = db.query(Solicitante).filter(
                Solicitante.IDENTIFICACION == sancion.IDENTIFICACION
            ).first()
            if solicitante:
                solicitante.ESTADO = 'apto'
        
        db.commit()
        
        return {"message": "Sanción marcada como cumplida exitosamente"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al cumplir sanción: {str(e)}")

@router.put("/{sancion_id}/cancelar")
def cancelar_sancion(sancion_id: int, db: Session = Depends(get_db)):
    """Cancelar una sanción y restaurar el estado del solicitante"""
    try:
        sancion = db.query(Sancion).filter(Sancion.IDSANCION == sancion_id).first()
        if not sancion:
            raise HTTPException(status_code=404, detail="Sanción no encontrada")
        
        if sancion.ESTADO == 'cancelada':
            raise HTTPException(status_code=400, detail="La sanción ya está cancelada")
        
        # Cancelar sanción
        sancion.ESTADO = 'cancelada'
        
        # Verificar si el solicitante tiene otras sanciones activas
        otras_sanciones_activas = db.query(Sancion).filter(
            Sancion.IDENTIFICACION == sancion.IDENTIFICACION,
            Sancion.ESTADO == 'activa',
            Sancion.IDSANCION != sancion_id
        ).count()
        
        # Si no tiene otras sanciones activas, restaurar estado a 'apto'
        if otras_sanciones_activas == 0:
            solicitante = db.query(Solicitante).filter(
                Solicitante.IDENTIFICACION == sancion.IDENTIFICACION
            ).first()
            if solicitante:
                solicitante.ESTADO = 'apto'
        
        db.commit()
        
        return {"message": "Sanción cancelada exitosamente"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al cancelar sanción: {str(e)}")

@router.get("/vencidas")
def verificar_sanciones_vencidas(db: Session = Depends(get_db)):
    """Verificar y actualizar sanciones que han vencido automáticamente"""
    try:
        hoy = date.today()
        
        # Buscar sanciones activas que ya vencieron
        sanciones_vencidas = db.query(Sancion).filter(
            Sancion.ESTADO == 'activa',
            Sancion.FECHA_FIN < hoy
        ).all()
        
        sanciones_actualizadas = []
        
        for sancion in sanciones_vencidas:
            # Marcar como cumplida
            sancion.ESTADO = 'cumplida'
            
            # Verificar si el solicitante tiene otras sanciones activas
            otras_sanciones_activas = db.query(Sancion).filter(
                Sancion.IDENTIFICACION == sancion.IDENTIFICACION,
                Sancion.ESTADO == 'activa',
                Sancion.IDSANCION != sancion.IDSANCION
            ).count()
            
            # Si no tiene otras sanciones activas, restaurar estado a 'apto'
            if otras_sanciones_activas == 0:
                solicitante = db.query(Solicitante).filter(
                    Solicitante.IDENTIFICACION == sancion.IDENTIFICACION
                ).first()
                if solicitante:
                    solicitante.ESTADO = 'apto'
            
            sanciones_actualizadas.append(sancion.IDSANCION)
        
        db.commit()
        
        return {
            "message": f"Se actualizaron {len(sanciones_actualizadas)} sanciones vencidas",
            "sanciones_actualizadas": sanciones_actualizadas
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al verificar sanciones vencidas: {str(e)}")
