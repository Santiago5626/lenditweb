from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from entidades.modelos.solicitante_modelo import (
    SolicitanteAprendiz,
    SolicitanteEmpleado,
    SolicitanteResponse,
    EliminarSolicitante,
    RolEnum
)
from entidades.baseDatos.solicitante import Solicitante
from entidades.baseDatos.db import SessionLocal
from typing import List
from fastapi.encoders import jsonable_encoder
from entidades.funciones.login import verify_jwt_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/obtener")
async def obtener_solicitantes(db: Session = Depends(get_db), token: str = Depends(verify_jwt_token)):
    try:
        solicitantes = db.query(Solicitante).all()
        
        if not solicitantes:
            return JSONResponse(
                status_code=200,
                content=[]
            )
        
        # Convertir los objetos SQLAlchemy a diccionarios
        solicitantes_list = []
        for solicitante in solicitantes:
            solicitante_dict = {
                "identificacion": solicitante.identificacion,
                "primer_nombre": solicitante.primer_nombre,
                "segundo_nombre": solicitante.segundo_nombre,
                "primer_apellido": solicitante.primer_apellido,
                "segundo_apellido": solicitante.segundo_apellido,
                "correo": solicitante.correo,
                "telefono": solicitante.telefono,
                "genero": solicitante.genero,
                "rol": solicitante.rol,
                "ficha": solicitante.ficha if solicitante.rol == 'aprendiz' else None,
                "programa": solicitante.programa if solicitante.rol == 'aprendiz' else None
            }
            solicitantes_list.append(solicitante_dict)

        return JSONResponse(
            status_code=200,
            content=solicitantes_list
        )
    except Exception as e:
        print(f"Error al obtener solicitantes: {str(e)}")  # Log del error
        return JSONResponse(
            status_code=500,
            content={"detail": f"Error al obtener los solicitantes: {str(e)}"}
        )

@router.post("/registrar")
async def registrar_solicitante(
    solicitante: SolicitanteAprendiz | SolicitanteEmpleado,
    db: Session = Depends(get_db),
    token: str = Depends(verify_jwt_token)
):
    try:
        # Verificar si ya existe
        existing_user = db.query(Solicitante).filter(
            Solicitante.identificacion == solicitante.identificacion
        ).first()
        
        if existing_user:
            return JSONResponse(
                status_code=400,
                content={"detail": "Este solicitante ya existe"}
            )

        # Crear nuevo solicitante
        nuevo_solicitante = Solicitante(
            identificacion=solicitante.identificacion,
            primer_nombre=solicitante.primer_nombre,
            segundo_nombre=solicitante.segundo_nombre,
            primer_apellido=solicitante.primer_apellido,
            segundo_apellido=solicitante.segundo_apellido,
            correo=solicitante.correo,
            telefono=solicitante.telefono,
            genero=solicitante.genero.value,  # Convertir enum a string
            rol=solicitante.rol.value  # Convertir enum a string
        )

        # Agregar campos específicos si es aprendiz
        if solicitante.rol == RolEnum.APRENDIZ:
            if isinstance(solicitante, SolicitanteAprendiz):
                nuevo_solicitante.ficha = solicitante.ficha
                nuevo_solicitante.programa = solicitante.programa
            else:
                return JSONResponse(
                    status_code=400,
                    content={"detail": "Los campos ficha y programa son requeridos para aprendices"}
                )

        db.add(nuevo_solicitante)
        db.commit()
        db.refresh(nuevo_solicitante)
        
        return JSONResponse(
            status_code=201,
            content={"detail": "Solicitante registrado exitosamente"}
        )
    except Exception as e:
        db.rollback()
        print(f"Error al registrar solicitante: {str(e)}")  # Log del error
        return JSONResponse(
            status_code=500,
            content={"detail": f"Error al registrar: {str(e)}"}
        )

@router.put("/actualizar")
async def actualizar_solicitante(
    solicitante: SolicitanteAprendiz | SolicitanteEmpleado,
    db: Session = Depends(get_db),
    token: str = Depends(verify_jwt_token)
):
    try:
        existing_user = db.query(Solicitante).filter(
            Solicitante.identificacion == solicitante.identificacion
        ).first()

        if not existing_user:
            return JSONResponse(
                status_code=404,
                content={"detail": "Solicitante no encontrado"}
            )

        update_data = {
            "primer_nombre": solicitante.primer_nombre,
            "segundo_nombre": solicitante.segundo_nombre,
            "primer_apellido": solicitante.primer_apellido,
            "segundo_apellido": solicitante.segundo_apellido,
            "correo": solicitante.correo,
            "telefono": solicitante.telefono,
            "genero": solicitante.genero.value,  # Convertir enum a string
            "rol": solicitante.rol.value  # Convertir enum a string
        }

        if solicitante.rol == RolEnum.APRENDIZ:
            if isinstance(solicitante, SolicitanteAprendiz):
                update_data["ficha"] = solicitante.ficha
                update_data["programa"] = solicitante.programa
            else:
                return JSONResponse(
                    status_code=400,
                    content={"detail": "Los campos ficha y programa son requeridos para aprendices"}
                )
        else:
            update_data["ficha"] = None
            update_data["programa"] = None

        db.query(Solicitante).filter(
            Solicitante.identificacion == solicitante.identificacion
        ).update(update_data)
        db.commit()
        
        return JSONResponse(
            status_code=200,
            content={"detail": "Solicitante actualizado exitosamente"}
        )
    except Exception as e:
        db.rollback()
        print(f"Error al actualizar solicitante: {str(e)}")  # Log del error
        return JSONResponse(
            status_code=500,
            content={"detail": f"Error al actualizar: {str(e)}"}
        )

@router.delete("/eliminar")
async def eliminar_solicitante(
    solicitante: EliminarSolicitante,
    db: Session = Depends(get_db),
    token: str = Depends(verify_jwt_token)
):
    try:
        existing_user = db.query(Solicitante).filter(
            Solicitante.identificacion == solicitante.identificacion
        ).first()

        if not existing_user:
            return JSONResponse(
                status_code=404,
                content={"detail": "Solicitante no existe"}
            )

        db.query(Solicitante).filter(
            Solicitante.identificacion == solicitante.identificacion
        ).delete()
        db.commit()
        
        return JSONResponse(
            status_code=200,
            content={"detail": "Solicitante eliminado exitosamente"}
        )
    except Exception as e:
        db.rollback()
        print(f"Error al eliminar solicitante: {str(e)}")  # Log del error
        return JSONResponse(
            status_code=500,
            content={"detail": f"Error al eliminar: {str(e)}"}
        )
