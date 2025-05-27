from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Response, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from entidades.modelos.solicitante_modelo import (
    SolicitanteAprendiz,
    SolicitanteResponse,
    EliminarSolicitante,
    UpdateSolicitante,
    RolEnum,
)
from typing import List
from fastapi.responses import JSONResponse
import pandas as pd
import io
from entidades.baseDatos.solicitante import Solicitante
from entidades.baseDatos.db import SessionLocal
from typing import List
from fastapi.encoders import jsonable_encoder
from entidades.funciones.login import verify_jwt_token

router = APIRouter()

@router.put("/actualizar")
async def actualizar_solicitante(
    solicitante: UpdateSolicitante,
    token: str = Depends(verify_jwt_token)
):
    db = SessionLocal()
    try:
        solicitante_db = db.query(Solicitante).filter_by(identificacion=solicitante.identificacion).first()
        if not solicitante_db:
            return JSONResponse(
                status_code=404,
                content={"detail": f"No se encontró el solicitante con identificación {solicitante.identificacion}"}
            )

        # Validar campos requeridos para aprendices
        if solicitante.rol == RolEnum.APRENDIZ:
            if not solicitante.ficha or not solicitante.programa:
                return JSONResponse(
                    status_code=400,
                    content={"detail": "Los campos 'ficha' y 'programa' son requeridos para aprendices"}
                )
        
        # Actualizar campos
        solicitante_db.primer_nombre = solicitante.primer_nombre.strip().upper()
        solicitante_db.segundo_nombre = solicitante.segundo_nombre.strip().upper() if solicitante.segundo_nombre else None
        solicitante_db.primer_apellido = solicitante.primer_apellido.strip().upper()
        solicitante_db.segundo_apellido = solicitante.segundo_apellido.strip().upper() if solicitante.segundo_apellido else None
        solicitante_db.correo = solicitante.correo.strip().upper()
        solicitante_db.telefono = solicitante.telefono
        solicitante_db.rol = solicitante.rol
        solicitante_db.ficha = solicitante.ficha.strip().upper() if solicitante.ficha else None
        solicitante_db.programa = solicitante.programa.strip().upper() if solicitante.programa else None

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
    solicitante: EliminarSolicitante,
    token: str = Depends(verify_jwt_token)
):
    db = SessionLocal()
    try:
        solicitante_db = db.query(Solicitante).filter_by(identificacion=solicitante.identificacion).first()
        if not solicitante_db:
            return JSONResponse(
                status_code=404,
                content={"detail": f"No se encontró el solicitante con identificación {solicitante.identificacion}"}
            )
        
        db.delete(solicitante_db)
        db.commit()
        return JSONResponse(
            status_code=200,
            content={"detail": f"Solicitante con identificación {solicitante.identificacion} eliminado exitosamente"}
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar solicitante: {str(e)}")
    finally:
        db.close()

@router.get("/obtener", response_model=List[SolicitanteResponse])
def obtener_solicitantes(token: str = Depends(verify_jwt_token)):
    db = SessionLocal()
    try:
        solicitantes = db.query(Solicitante).all()
        print(f"Solicitantes encontrados: {len(solicitantes)}")
        if not solicitantes:
            print("No se encontraron solicitantes")
            return []
            
        result = []
        for s in solicitantes:
            print(f"Procesando solicitante: {s.identificacion}")
            solicitante_dict = {
                "identificacion": s.identificacion,
                "primer_nombre": s.primer_nombre,
                "segundo_nombre": s.segundo_nombre,
                "primer_apellido": s.primer_apellido,
                "segundo_apellido": s.segundo_apellido,
                "correo": s.correo,
                "telefono": s.telefono,
                "rol": s.rol,
                "ficha": s.ficha,
                "programa": s.programa
            }
            result.append(solicitante_dict)
        
        print(f"Resultado final: {result}")
        return result
    except Exception as e:
        print(f"Error al obtener solicitantes: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al obtener solicitantes: {str(e)}")
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

@router.post("/importar-excel")
async def importar_solicitantes(
    file: UploadFile = File(...),
    token: str = Depends(verify_jwt_token)
):
    if not file.filename.endswith('.xlsx'):
        return JSONResponse(
            status_code=400,
            content={"detail": "El archivo debe ser un Excel (.xlsx)"}
        )

    try:
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": f"Error al leer el archivo Excel: {str(e)}"}
        )

    db = SessionLocal()
    solicitantes_creados = 0
    errores = []

    required_columns = [
        'Número de documento',
        'Nombre completo',
        'Número de teléfono',
        'Correo electrónico',
        'Tipo de rol'
    ]

    for col in required_columns:
        if col not in df.columns:
            db.close()
            return JSONResponse(
                status_code=400,
                content={"detail": f"Columna requerida '{col}' no encontrada en el Excel"}
            )

    for index, row in df.iterrows():
        try:
            nombres = str(row['Nombre completo']).strip().upper().split()
            if len(nombres) < 2:
                raise ValueError("El nombre completo debe contener al menos un nombre y un apellido")

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
            else:
                primer_nombre = nombres[0]
                segundo_nombre = None
                primer_apellido = nombres[1]
                segundo_apellido = None

            # Normalizar el rol
            rol = str(row['Tipo de rol']).strip().lower()
            # Eliminar punto final si existe
            rol = rol.rstrip('.')
            valid_roles = ['aprendiz', 'contratista', 'funcionario', 'instructor']
            if rol not in valid_roles:
                raise ValueError(f"Rol inválido: '{rol}'. Debe ser uno de: {', '.join(valid_roles)}")

            telefono = str(row['Número de teléfono'])
            if 'E' in telefono or 'e' in telefono:
                telefono = str(int(float(telefono)))

            telefono_validado = validate_phone(telefono)
            if telefono_validado is None:
                raise ValueError("Número de teléfono inválido")

            solicitante_data = {
                'identificacion': str(row['Número de documento']).strip().upper().rstrip('.'),
                'primer_nombre': primer_nombre.rstrip('.'),
                'segundo_nombre': segundo_nombre.rstrip('.') if segundo_nombre else None,
                'primer_apellido': primer_apellido.rstrip('.'),
                'segundo_apellido': segundo_apellido.rstrip('.') if segundo_apellido else None,
                'correo': str(row['Correo electrónico']).strip().upper().rstrip('.'),
                'telefono': telefono_validado,
                'rol': rol
            }

            if rol == 'aprendiz':
                if pd.isna(row.get('Número de ficha')) or pd.isna(row.get('Programa de formación')):
                    raise ValueError("Los campos 'Número de ficha' y 'Programa de formación' son requeridos para aprendices")
                solicitante_data['ficha'] = str(row['Número de ficha']).strip().upper()
                solicitante_data['programa'] = str(row['Programa de formación']).strip().upper()

            existing = db.query(Solicitante).filter_by(identificacion=solicitante_data['identificacion']).first()
            if existing:
                errores.append(f"Fila {index + 2}: Solicitante con identificación {solicitante_data['identificacion']} ya existe")
                continue

            try:
                nuevo_solicitante = Solicitante(**solicitante_data)
                db.add(nuevo_solicitante)
                db.flush()
                solicitantes_creados += 1
            except Exception as e:
                errores.append(f"Error en fila {index + 2}: {str(e)}")

        except Exception as e:
            errores.append(f"Error en fila {index + 2}: {str(e)}")

    if not errores:
        try:
            db.commit()
            return JSONResponse(
                status_code=200,
                content={"detail": f"Se importaron {solicitantes_creados} solicitantes exitosamente"}
            )
        except Exception as e:
            db.rollback()
            return JSONResponse(
                status_code=500,
                content={"detail": f"Error al guardar los cambios: {str(e)}"}
            )
    else:
        db.rollback()
        return JSONResponse(
            status_code=400,
            content={
                "detail": f"Se encontraron {len(errores)} errores durante la importación",
                "errores": errores
            }
        )
    db.close()
