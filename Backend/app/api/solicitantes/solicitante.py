from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Response, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.schemas.solicitante_modelo import (
    SolicitanteAprendiz,
    SolicitanteResponse,
    EliminarSolicitante,
    EliminarMultiplesSolicitantes,
    UpdateSolicitante,
    RolEnum,
)
from typing import List
import pandas as pd
import io
from app.core.database.solicitante import Solicitante
from app.core.database.programas import Programas
from app.core.database.ficha import Ficha
from app.core.database.db import SessionLocal
from fastapi.encoders import jsonable_encoder
from app.api.auth.login import verify_jwt_token

router = APIRouter()

@router.post("/importar-excel")
async def importar_solicitantes_excel(
    file: UploadFile = File(...),
    token: str = Depends(verify_jwt_token)
):
    if not file.filename.endswith('.xlsx'):
        return JSONResponse(
            status_code=400,
            content={"detail": "El archivo debe ser un archivo Excel (.xlsx)"}
        )

    db = SessionLocal()
    try:
        # Leer el archivo Excel
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))

        # Validar las columnas requeridas
        columnas_requeridas = [
            "Nombre completo",
            "Número de documento",
            "Número de teléfono",
            "Tipo de rol",
            "Número de ficha",
            "Programa de formación"
        ]
        columnas_disponibles = df.columns.tolist()
        
        # Verificar si todas las columnas requeridas están presentes
        columnas_faltantes = [col for col in columnas_requeridas if col not in columnas_disponibles]
        if columnas_faltantes:
            return JSONResponse(
                status_code=400,
                content={
                    "detail": "Formato de archivo inválido",
                    "columnas_requeridas": columnas_requeridas,
                    "columnas_disponibles": columnas_disponibles
                }
            )

        total_procesados = 0
        exitosos = 0
        errores = []
        
        # Procesar cada fila de forma independiente
        for index, row in df.iterrows():
            # Crear una nueva transacción para cada fila
            db_transaction = SessionLocal()
            try:
                total_procesados += 1
                
                # Extraer y validar datos
                nombre_completo = str(row["Nombre completo"]).strip()
                # Limpiar caracteres especiales del nombre
                nombre_completo = nombre_completo.rstrip('.,;:!?').strip()
                nombres = nombre_completo.split()
                
                # Asignar nombres y apellidos
                if len(nombres) >= 4:
                    primer_nombre = nombres[0]
                    segundo_nombre = nombres[1]
                    primer_apellido = nombres[2]
                    segundo_apellido = nombres[3]
                elif len(nombres) == 3:
                    primer_nombre = nombres[0]
                    segundo_nombre = None
                    primer_apellido = nombres[1]
                    segundo_apellido = nombres[2]
                elif len(nombres) == 2:
                    primer_nombre = nombres[0]
                    segundo_nombre = None
                    primer_apellido = nombres[1]
                    segundo_apellido = None
                else:
                    raise ValueError("El nombre completo debe tener al menos nombre y apellido")

                identificacion = str(row["Número de documento"]).strip()
                # Limpiar caracteres especiales del documento
                identificacion = identificacion.rstrip('.,;:!?').strip()
                if not identificacion.isdigit():
                    raise ValueError("El número de documento debe contener solo dígitos")

                telefono = validate_phone(row["Número de teléfono"])
                if not telefono:
                    raise ValueError("Número de teléfono inválido (debe tener 10 dígitos y empezar con 3)")

                rol = str(row["Tipo de rol"]).strip().lower()
                # Limpiar caracteres especiales del rol
                rol = rol.rstrip('.,;:!?').strip()
                if rol not in ['aprendiz', 'contratista', 'funcionario', 'instructor']:
                    raise ValueError("Tipo de rol inválido (debe ser: aprendiz, contratista, funcionario o instructor)")

                # Validar campos específicos para aprendices
                ficha = str(row["Número de ficha"]).strip().rstrip('.,;:!?').strip() if pd.notna(row["Número de ficha"]) else None
                programa = str(row["Programa de formación"]).strip().rstrip('.,;:!?').strip() if pd.notna(row["Programa de formación"]) else None

                if rol == 'aprendiz':
                    if not ficha or not programa:
                        raise ValueError("Los campos 'Número de ficha' y 'Programa de formación' son obligatorios para aprendices")

                # Preparar datos del solicitante
                solicitante_data = {
                    'IDENTIFICACION': identificacion.upper(),
                    'PRIMER_NOMBRE': primer_nombre.upper(),
                    'SEGUNDO_NOMBRE': segundo_nombre.upper() if segundo_nombre else None,
                    'PRIMER_APELLIDO': primer_apellido.upper(),
                    'SEGUNDO_APELLIDO': segundo_apellido.upper() if segundo_apellido else None,
                    'CORREO': str(row.get("Correo electrónico", "")).strip().rstrip('.,;:!?').strip().upper() if pd.notna(row.get("Correo electrónico")) else None,
                    'TELEFONO': telefono,
                    'ROL': rol,
                    'ESTADO': 'apto'
                }

                # Manejar ficha y programa
                if rol == 'aprendiz':
                    # Buscar o crear el programa
                    programa_obj = db_transaction.query(Programas).filter_by(NOMBRE_PROGRAMA=programa.upper()).first()
                    if not programa_obj:
                        last_program = db_transaction.query(Programas).order_by(Programas.CODPROGRAMA.desc()).first()
                        new_num = 1 if not last_program else int(last_program.CODPROGRAMA[4:]) + 1
                        new_code = f"PROG{new_num:04d}"
                        programa_obj = Programas(CODPROGRAMA=new_code, NOMBRE_PROGRAMA=programa.upper())
                        db_transaction.add(programa_obj)
                        db_transaction.flush()

                    # Buscar o crear la ficha
                    ficha_obj = db_transaction.query(Ficha).filter_by(CODFICHA=ficha).first()
                    if not ficha_obj:
                        ficha_obj = Ficha(CODFICHA=ficha, CODPROGRAMA=programa_obj.CODPROGRAMA)
                        db_transaction.add(ficha_obj)
                        db_transaction.flush()
                    elif ficha_obj.CODPROGRAMA != programa_obj.CODPROGRAMA:
                        raise ValueError(f"La ficha {ficha} ya está asociada a otro programa")

                    solicitante_data['FICHA'] = ficha

                # Verificar si ya existe un solicitante con la misma identificación
                existing = db_transaction.query(Solicitante).filter_by(IDENTIFICACION=identificacion.upper()).first()
                if existing:
                    raise ValueError(f"Ya existe un solicitante con la identificación {identificacion}")

                # Crear el solicitante
                nuevo_solicitante = Solicitante(**solicitante_data)
                db_transaction.add(nuevo_solicitante)
                
                # Commit de esta transacción específica
                db_transaction.commit()
                exitosos += 1

            except Exception as e:
                errores.append(f"Fila {index + 2}: {str(e)}")
                db_transaction.rollback()
            finally:
                db_transaction.close()


        return JSONResponse(
            status_code=200,
            content={
                "total_procesados": total_procesados,
                "exitosos": exitosos,
                "errores": errores,
                "parcial": len(errores) > 0 and exitosos > 0
            }
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"detail": f"Error al procesar el archivo: {str(e)}"}
        )
    finally:
        db.close()


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
            'IDENTIFICACION': solicitante.identificacion.strip().rstrip('.,;:!?').strip().upper(),
            'PRIMER_NOMBRE': solicitante.primer_nombre.strip().rstrip('.,;:!?').strip().upper(),
            'SEGUNDO_NOMBRE': solicitante.segundo_nombre.strip().rstrip('.,;:!?').strip().upper() if solicitante.segundo_nombre else None,
            'PRIMER_APELLIDO': solicitante.primer_apellido.strip().rstrip('.,;:!?').strip().upper(),
            'SEGUNDO_APELLIDO': solicitante.segundo_apellido.strip().rstrip('.,;:!?').strip().upper() if solicitante.segundo_apellido else None,
            'CORREO': solicitante.correo.strip().rstrip('.,;:!?').strip().upper() if solicitante.correo else None,
            'TELEFONO': telefono_validado,
            'ROL': solicitante.rol,
            'ESTADO': 'apto'
        }

        # Manejar ficha y programa según el rol
        if solicitante.rol == RolEnum.APRENDIZ:
            ficha_codigo = solicitante.ficha.strip().rstrip('.,;:!?').strip().upper()
            programa_nombre = solicitante.programa.strip().rstrip('.,;:!?').strip().upper()
            
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
            programa_nombre = solicitante.programa.strip().rstrip('.,;:!?').strip().upper()
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
        solicitantes = db.query(Solicitante).order_by(Solicitante.IDENTIFICACION.desc()).all()
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

@router.put("/actualizar")
async def actualizar_solicitante(
    solicitante: UpdateSolicitante,
    token: str = Depends(verify_jwt_token)
):
    db = SessionLocal()
    try:
        # Buscar el solicitante existente
        existing = db.query(Solicitante).filter_by(IDENTIFICACION=solicitante.identificacion).first()
        if not existing:
            return JSONResponse(
                status_code=404,
                content={"detail": f"No se encontró un solicitante con la identificación {solicitante.identificacion}"}
            )

        # Validar el teléfono
        telefono_validado = validate_phone(solicitante.telefono)
        if telefono_validado is None:
            return JSONResponse(
                status_code=400,
                content={"detail": "Número de teléfono inválido"}
            )

        # Actualizar los campos
        existing.PRIMER_NOMBRE = solicitante.primer_nombre.strip().rstrip('.,;:!?').strip().upper()
        existing.SEGUNDO_NOMBRE = solicitante.segundo_nombre.strip().rstrip('.,;:!?').strip().upper() if solicitante.segundo_nombre else None
        existing.PRIMER_APELLIDO = solicitante.primer_apellido.strip().rstrip('.,;:!?').strip().upper()
        existing.SEGUNDO_APELLIDO = solicitante.segundo_apellido.strip().rstrip('.,;:!?').strip().upper() if solicitante.segundo_apellido else None
        existing.CORREO = solicitante.correo.strip().rstrip('.,;:!?').strip().upper() if solicitante.correo else None
        existing.TELEFONO = telefono_validado
        existing.ROL = solicitante.rol

        # Manejar ficha y programa según el rol
        if solicitante.rol == RolEnum.APRENDIZ:
            if not solicitante.ficha or not solicitante.programa:
                return JSONResponse(
                    status_code=400,
                    content={"detail": "Los campos 'ficha' y 'programa' son requeridos para aprendices"}
                )
            
            ficha_codigo = solicitante.ficha.strip().rstrip('.,;:!?').strip().upper()
            programa_nombre = solicitante.programa.strip().rstrip('.,;:!?').strip().upper()
            
            # Buscar o crear el programa
            programa = db.query(Programas).filter_by(NOMBRE_PROGRAMA=programa_nombre).first()
            if not programa:
                last_program = db.query(Programas).order_by(Programas.CODPROGRAMA.desc()).first()
                new_num = 1 if not last_program else int(last_program.CODPROGRAMA[4:]) + 1
                new_code = f"PROG{new_num:04d}"
                programa = Programas(CODPROGRAMA=new_code, NOMBRE_PROGRAMA=programa_nombre)
                db.add(programa)
                db.flush()
            
            # Buscar o crear la ficha
            ficha = db.query(Ficha).filter_by(CODFICHA=ficha_codigo).first()
            if not ficha:
                ficha = Ficha(CODFICHA=ficha_codigo, CODPROGRAMA=programa.CODPROGRAMA)
                db.add(ficha)
                db.flush()
            elif ficha.CODPROGRAMA != programa.CODPROGRAMA:
                existing_programa = db.query(Programas).filter_by(CODPROGRAMA=ficha.CODPROGRAMA).first()
                programa_existente_nombre = existing_programa.NOMBRE_PROGRAMA if existing_programa else "programa desconocido"
                return JSONResponse(
                    status_code=400,
                    content={"detail": f"Este número de ficha ({ficha_codigo}) pertenece a otro programa: {programa_existente_nombre}"}
                )
            
            existing.FICHA = ficha_codigo
            existing.PROGRAMA = None
        elif solicitante.programa:
            # Para otros roles, crear programa si no existe
            programa_nombre = solicitante.programa.strip().rstrip('.,;:!?').strip().upper()
            programa = db.query(Programas).filter_by(NOMBRE_PROGRAMA=programa_nombre).first()
            if not programa:
                last_program = db.query(Programas).order_by(Programas.CODPROGRAMA.desc()).first()
                new_num = 1 if not last_program else int(last_program.CODPROGRAMA[4:]) + 1
                new_code = f"PROG{new_num:04d}"
                programa = Programas(CODPROGRAMA=new_code, NOMBRE_PROGRAMA=programa_nombre)
                db.add(programa)
                db.flush()
            
            existing.PROGRAMA = programa.CODPROGRAMA
            existing.FICHA = None

        db.commit()
        
        return JSONResponse(
            status_code=200,
            content={"detail": f"Solicitante con identificación {solicitante.identificacion} actualizado exitosamente"}
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar solicitante: {str(e)}")
    finally:
        db.close()

@router.delete("/eliminar")
async def eliminar_solicitante(
    request: EliminarSolicitante,
    token: str = Depends(verify_jwt_token)
):
    db = SessionLocal()
    try:
        # Buscar el solicitante
        solicitante = db.query(Solicitante).filter_by(IDENTIFICACION=request.identificacion).first()
        if not solicitante:
            return JSONResponse(
                status_code=404,
                content={"detail": f"No se encontró un solicitante con la identificación {request.identificacion}"}
            )

        # Eliminar el solicitante
        db.delete(solicitante)
        db.commit()
        
        return JSONResponse(
            status_code=200,
            content={"detail": f"Solicitante con identificación {request.identificacion} eliminado exitosamente"}
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar solicitante: {str(e)}")
    finally:
        db.close()

@router.delete("/eliminar-multiples")
async def eliminar_multiples_solicitantes(
    request: EliminarMultiplesSolicitantes,
    token: str = Depends(verify_jwt_token)
):
    db = SessionLocal()
    try:
        eliminados = 0
        errores = []
        
        for identificacion in request.identificaciones:
            try:
                solicitante = db.query(Solicitante).filter_by(IDENTIFICACION=identificacion).first()
                if solicitante:
                    db.delete(solicitante)
                    eliminados += 1
                else:
                    errores.append(f"No se encontró solicitante con identificación {identificacion}")
            except Exception as e:
                errores.append(f"Error al eliminar {identificacion}: {str(e)}")
        
        db.commit()
        
        return JSONResponse(
            status_code=200,
            content={
                "detail": f"Se eliminaron {eliminados} solicitantes exitosamente",
                "eliminados": eliminados,
                "errores": errores
            }
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar solicitantes: {str(e)}")
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
