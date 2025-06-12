from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Response, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.schemas.solicitante_modelo import (
    SolicitanteAprendiz,
    SolicitanteResponse,
    EliminarSolicitante,
    EliminarMultiplesSolicitantes,
    UpdateSolicitante,
    RolEnum,
)
from typing import List
from fastapi.responses import JSONResponse
import pandas as pd
import io
from app.core.database.solicitante import Solicitante
from app.core.database.programas import Programas
from app.core.database.ficha import Ficha
from app.core.database.db import SessionLocal
from fastapi.encoders import jsonable_encoder
from app.api.auth.login import verify_jwt_token

router = APIRouter()

@router.post("/registrar")
async def registrar_solicitante(
    solicitante: SolicitanteResponse,
    token: str = Depends(verify_jwt_token)
):
    db = SessionLocal()
    try:
        # Verificar si ya existe un solicitante con la misma identificación
        existing = db.query(Solicitante).filter_by(IDENTIFICACION=solicitante.identificacion).first()
        if existing:
            return JSONResponse(
                status_code=400,
                content={"detail": f"Ya existe un solicitante con la identificación {solicitante.identificacion}"}
            )

        # Validar el teléfono
        telefono_validado = validate_phone(solicitante.telefono)
        if telefono_validado is None:
            return JSONResponse(
                status_code=400,
                content={"detail": "Número de teléfono inválido"}
            )

        # Validar campos requeridos para aprendices
        if solicitante.rol == RolEnum.APRENDIZ:
            if not solicitante.ficha or not solicitante.programa:
                return JSONResponse(
                    status_code=400,
                    content={"detail": "Los campos 'ficha' y 'programa' son requeridos para aprendices"}
                )

        # Preparar datos del solicitante
        solicitante_data = {
            'IDENTIFICACION': solicitante.identificacion.strip().upper(),
            'PRIMER_NOMBRE': solicitante.primer_nombre.strip().upper(),
            'SEGUNDO_NOMBRE': solicitante.segundo_nombre.strip().upper() if solicitante.segundo_nombre else None,
            'PRIMER_APELLIDO': solicitante.primer_apellido.strip().upper(),
            'SEGUNDO_APELLIDO': solicitante.segundo_apellido.strip().upper() if solicitante.segundo_apellido else None,
            'CORREO': solicitante.correo.strip().upper() if solicitante.correo else None,
            'TELEFONO': telefono_validado,
            'ROL': solicitante.rol,
            'ESTADO': 'apto'
        }

        # Manejar ficha y programa según el rol
        if solicitante.rol == RolEnum.APRENDIZ:
            ficha_codigo = solicitante.ficha.strip().upper()
            programa_nombre = solicitante.programa.strip().upper()
            
            # Buscar o crear el programa
            programa = db.query(Programas).filter_by(NOMBRE_PROGRAMA=programa_nombre).first()
            if not programa:
                # Generar un código autoincremental para el programa
                last_program = db.query(Programas).order_by(Programas.CODPROGRAMA.desc()).first()
                if last_program:
                    # Extraer el número del último código y aumentarlo en 1
                    try:
                        last_num = int(last_program.CODPROGRAMA[4:])  # Tomar los dígitos después de 'PROG'
                        new_num = last_num + 1
                    except ValueError:
                        new_num = 1
                else:
                    new_num = 1
                
                new_code = f"PROG{new_num:04d}"  # Formato: PROG0001, PROG0002, etc.
                
                programa = Programas(
                    CODPROGRAMA=new_code,
                    NOMBRE_PROGRAMA=programa_nombre
                )
                db.add(programa)
                db.flush()
            
            # Buscar o crear la ficha
            ficha = db.query(Ficha).filter_by(CODFICHA=ficha_codigo).first()
            if not ficha:
                ficha = Ficha(
                    CODFICHA=ficha_codigo,
                    CODPROGRAMA=programa.CODPROGRAMA
                )
                db.add(ficha)
                db.flush()
            else:
                # Verificar si la ficha pertenece a un programa diferente
                if ficha.CODPROGRAMA != programa.CODPROGRAMA:
                    existing_programa = db.query(Programas).filter_by(CODPROGRAMA=ficha.CODPROGRAMA).first()
                    programa_existente_nombre = existing_programa.NOMBRE_PROGRAMA if existing_programa else "programa desconocido"
                    return JSONResponse(
                        status_code=400,
                        content={"detail": f"Este número de ficha ({ficha_codigo}) pertenece a otro programa: {programa_existente_nombre}"}
                    )
            
            solicitante_data['FICHA'] = ficha_codigo
        elif solicitante.programa:
            # Para otros roles, crear programa si no existe
            programa_nombre = solicitante.programa.strip().upper()
            programa = db.query(Programas).filter_by(NOMBRE_PROGRAMA=programa_nombre).first()
            if not programa:
                programa = Programas(
                    CODPROGRAMA=f"PROG{len(programa_nombre)[:4]}",  # Código genérico
                    NOMBRE_PROGRAMA=programa_nombre
                )
                db.add(programa)
                db.flush()
            
            solicitante_data['PROGRAMA'] = programa.CODPROGRAMA

        # Crear el nuevo solicitante
        nuevo_solicitante = Solicitante(**solicitante_data)

        db.add(nuevo_solicitante)
        db.commit()
        
        return JSONResponse(
            status_code=201,
            content={"detail": f"Solicitante con identificación {solicitante.identificacion} creado exitosamente"}
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear solicitante: {str(e)}")
    finally:
        db.close()

@router.get("/obtener", response_model=List[SolicitanteResponse])
def obtener_solicitantes(token: str = Depends(verify_jwt_token)):
    db = SessionLocal()
    try:
        solicitantes = db.query(Solicitante).all()
        if not solicitantes:
            return []
            
        result = []
        for s in solicitantes:
            # Obtener información de ficha y programa
            ficha_info = None
            programa_info = None
            
            if s.ROL == 'aprendiz' and s.FICHA:
                ficha_info = s.FICHA
                if s.ficha and s.ficha.programa:
                    programa_info = s.ficha.programa.NOMBRE_PROGRAMA
            elif s.PROGRAMA and s.programa:
                programa_info = s.programa.NOMBRE_PROGRAMA
            
            solicitante_dict = {
                "identificacion": s.IDENTIFICACION,
                "primer_nombre": s.PRIMER_NOMBRE,
                "segundo_nombre": s.SEGUNDO_NOMBRE,
                "primer_apellido": s.PRIMER_APELLIDO,
                "segundo_apellido": s.SEGUNDO_APELLIDO,
                "correo": s.CORREO,
                "telefono": s.TELEFONO,
                "rol": s.ROL,
                "ficha": ficha_info,
                "programa": programa_info
            }
            result.append(solicitante_dict)
        
        return result
    except Exception as e:
        # Verificar si es un error de columna desconocida
        if "Unknown column" in str(e):
            # Extraer el nombre de la columna del mensaje de error
            import re
            match = re.search(r"Unknown column '([^']+)'", str(e))
            if match:
                columna = match.group(1)
                mensaje = f"La estructura de la base de datos no está actualizada. Falta la columna: {columna}. Por favor, reinicialice la base de datos."
            else:
                mensaje = "La estructura de la base de datos no está actualizada. Por favor, reinicialice la base de datos."
            raise HTTPException(status_code=500, detail=mensaje)
        else:
            raise HTTPException(status_code=500, detail="Error al obtener los solicitantes. Por favor, contacte al administrador del sistema.")
    finally:
        db.close()

def validate_phone(phone):
    """
    Valida el número de teléfono:
    - Debe empezar con 3
    - Debe tener 10 dígitos
    - Maneja números en notación científica
    - Elimina el código de país (57) si está presente
    - Maneja números con prefijo internacional (+57)
    Retorna None si no cumple con los criterios
    """
    try:
        # Convertir a string y limpiar
        phone = str(phone).strip().replace('.', '').replace(' ', '')
        
        # Manejar notación científica
        if 'E' in phone.upper():
            phone = str(int(float(phone)))
        
        # Remover prefijo internacional
        if phone.startswith('+57'):
            phone = phone[3:]
        elif phone.startswith('57'):
            phone = phone[2:]
            
        # Si el número tiene más de 10 dígitos, tomar los últimos 10
        if len(phone) > 10:
            phone = phone[-10:]
            
        # Validar formato final
        if len(phone) == 10 and phone.startswith('3') and phone.isdigit():
            return phone
            
        return None
    except:
        return None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
