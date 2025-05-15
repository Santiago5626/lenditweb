from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from entidades.modelos.solicitante_modelo import (
    SolicitanteAprendiz,
    SolicitanteEmpleado,
    SolicitanteResponse,
    EliminarSolicitante,
    RolEnum,
    GeneroEnum
)
import pandas as pd
import io
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

@router.post("/importar-excel")
async def importar_solicitantes(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith('.xlsx'):
        raise HTTPException(status_code=400, detail="El archivo debe ser un Excel (.xlsx)")
    
    try:
        # Leer el archivo Excel
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
        
        # Validar columnas requeridas
        required_columns = [
            'identificacion', 'primer_nombre', 'primer_apellido', 
            'correo', 'telefono', 'genero', 'rol'
        ]
        optional_columns = ['segundo_nombre', 'segundo_apellido', 'ficha', 'programa']
        
        for col in required_columns:
            if col not in df.columns:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Columna requerida '{col}' no encontrada en el Excel"
                )
        
        solicitantes_creados = 0
        errores = []
        
        # Procesar cada fila
        for index, row in df.iterrows():
            try:
                # Validar género
                genero = row['genero'].upper()
                if genero not in [e.value for e in GeneroEnum]:
                    raise ValueError(f"Género inválido: {genero}")
                
                # Validar rol
                rol = row['rol'].lower()
                if rol not in [e.value for e in RolEnum]:
                    raise ValueError(f"Rol inválido: {rol}")
                
                # Crear solicitante base
                solicitante_data = {
                    'identificacion': str(row['identificacion']).upper(),
                    'primer_nombre': str(row['primer_nombre']).upper(),
                    'primer_apellido': str(row['primer_apellido']).upper(),
                    'correo': str(row['correo']).upper(),
                    'telefono': str(row['telefono']),
                    'genero': genero,
                    'rol': rol
                }
                
                # Agregar campos opcionales si existen
                for campo in ['segundo_nombre', 'segundo_apellido']:
                    if campo in df.columns and pd.notna(row[campo]):
                        solicitante_data[campo] = str(row[campo]).upper()
                
                # Si es aprendiz, agregar campos adicionales
                if rol == 'aprendiz':
                    if 'ficha' not in df.columns or 'programa' not in df.columns:
                        raise ValueError("Campos 'ficha' y 'programa' son requeridos para aprendices")
                    solicitante_data['ficha'] = str(row['ficha']).upper()
                    solicitante_data['programa'] = str(row['programa']).upper()
                
                # Verificar si ya existe
                existing = db.query(Solicitante).filter_by(identificacion=solicitante_data['identificacion']).first()
                if existing:
                    errores.append(f"Fila {index + 2}: Solicitante con identificación {solicitante_data['identificacion']} ya existe")
                    continue
                
                # Crear nuevo solicitante
                nuevo_solicitante = Solicitante(**solicitante_data)
                db.add(nuevo_solicitante)
                solicitantes_creados += 1
                
            except Exception as e:
                errores.append(f"Error en fila {index + 2}: {str(e)}")
        
        # Commit solo si no hubo errores
        if not errores:
            db.commit()
            return {"message": f"Se importaron {solicitantes_creados} solicitantes exitosamente"}
        else:
            db.rollback()
            return {
                "message": f"Se encontraron {len(errores)} errores durante la importación",
                "errores": errores
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el archivo: {str(e)}")

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
            identificacion=str(solicitante.identificacion).upper(),
            primer_nombre=str(solicitante.primer_nombre).upper(),
            segundo_nombre=str(solicitante.segundo_nombre).upper() if solicitante.segundo_nombre else None,
            primer_apellido=str(solicitante.primer_apellido).upper(),
            segundo_apellido=str(solicitante.segundo_apellido).upper() if solicitante.segundo_apellido else None,
            correo=str(solicitante.correo).upper(),
            telefono=str(solicitante.telefono),
            genero=solicitante.genero.value,  # Convertir enum a string
            rol=solicitante.rol.value  # Convertir enum a string
        )

        # Agregar campos específicos si es aprendiz
        if solicitante.rol == RolEnum.APRENDIZ:
            if isinstance(solicitante, SolicitanteAprendiz):
                nuevo_solicitante.ficha = str(solicitante.ficha).upper()
                nuevo_solicitante.programa = str(solicitante.programa).upper()
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
            "primer_nombre": str(solicitante.primer_nombre).upper(),
            "segundo_nombre": str(solicitante.segundo_nombre).upper() if solicitante.segundo_nombre else None,
            "primer_apellido": str(solicitante.primer_apellido).upper(),
            "segundo_apellido": str(solicitante.segundo_apellido).upper() if solicitante.segundo_apellido else None,
            "correo": str(solicitante.correo).upper(),
            "telefono": str(solicitante.telefono),
            "genero": solicitante.genero.value,  # Convertir enum a string
            "rol": solicitante.rol.value  # Convertir enum a string
        }

        if solicitante.rol == RolEnum.APRENDIZ:
            if isinstance(solicitante, SolicitanteAprendiz):
                update_data["ficha"] = str(solicitante.ficha).upper()
                update_data["programa"] = str(solicitante.programa).upper()
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
