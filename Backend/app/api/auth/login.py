# routers/login.py
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.schemas.usuario_modelo import Login, Usuario as UsuarioModel
from app.core.database.usuario import Usuario
from app.core.database.db import SessionLocal
import jwt
from datetime import datetime, timedelta

router = APIRouter()

JWT_SECRET = "your_jwt_secret_key"  
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS = 3600  # Token expiracion (1 hora)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_jwt_token(user_id: int, nombre: str):
    payload = {
        "user_id": user_id,
        "nombre": nombre,
        "exp": datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

@router.post("/login")
async def login_user(user: Login, db: Session = Depends(get_db)):
    try:
        # Verificar si existen usuarios en la base de datos
        user_count = db.query(Usuario).count()
        if user_count == 0:
            # Si no hay usuarios, crear el admin
            try:
                admin_user = Usuario(
                    NOMBRE_USUARIO="admin",
                    EMAIL="admin@lendit.com",
                    PASSWORD="admin",
                    CC="1234567890",
                    ROL="administrador",
                    ESTADO="1"
                )
                db.add(admin_user)
                db.commit()
                print("Usuario admin creado exitosamente")
            except Exception as admin_error:
                db.rollback()
                print(f"Error al crear usuario admin: {str(admin_error)}")
            
        # Buscar el usuario por nombre o cc
        existing_user = db.query(Usuario).filter(
            (Usuario.NOMBRE_USUARIO == user.nombre) | (Usuario.CC == user.nombre)
        ).first()

        # Verificar si el usuario existe
        if not existing_user:
            return JSONResponse(
                status_code=404,
                content={
                    "detail": "Usuario no encontrado",
                    "success": False
                }
            )

        # Verificar la contraseña
        if existing_user.PASSWORD == user.password:
            token = create_jwt_token(existing_user.IDUSUARIO, existing_user.NOMBRE_USUARIO)
            return JSONResponse(
                status_code=200,
                content={
                    "detail": "Login exitoso",
                    "success": True,
                    "token": token,
                    "user": {
                        "nombre": existing_user.NOMBRE_USUARIO,
                        "rol": existing_user.ROL,
                        "cc": existing_user.CC
                    }
                }
            )
        else:
            return JSONResponse(
                status_code=401,
                content={
                    "detail": "Contraseña incorrecta",
                    "success": False
                }
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "detail": f"Error en el servidor: {str(e)}",
                "success": False
            }
        )

@router.post("/registrar")
async def registrar_usuario(user: UsuarioModel, db: Session = Depends(get_db)):
    try:
        # Verificar si el usuario ya existe por CC o email
        existing_user = db.query(Usuario).filter(
            (Usuario.CC == user.cc) | (Usuario.EMAIL == user.email)
        ).first()

        if existing_user:
            return JSONResponse(
                status_code=400,
                content={
                    "detail": "Usuario ya existe",
                    "success": False
                }
            )

        # Crear nuevo usuario
        new_user = Usuario(
            NOMBRE_USUARIO=user.nombre,
            EMAIL=user.email,
            PASSWORD=user.password,
            CC=user.cc,
            ROL=user.rol,
            ESTADO="1"
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return JSONResponse(
            status_code=201,
            content={
                "detail": "Usuario registrado exitosamente",
                "success": True
            }
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={
                "detail": f"Error al registrar: {str(e)}",
                "success": False
            }
        )

@router.get("/verify-token")
async def verify_token(credentials: HTTPAuthorizationCredentials = Security(HTTPBearer())):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return JSONResponse(
            status_code=200,
            content={
                "detail": "Token válido",
                "success": True
            }
        )
    except jwt.ExpiredSignatureError:
        return JSONResponse(
            status_code=401,
            content={
                "detail": "Token expirado",
                "success": False
            }
        )
    except jwt.InvalidTokenError:
        return JSONResponse(
            status_code=401,
            content={
                "detail": "Token inválido",
                "success": False
            }
        )

@router.post("/refresh-token")
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()), db: Session = Depends(get_db)):
    try:
        token = credentials.credentials
        
        # Decodificar el token actual (incluso si está expirado)
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            # Si el token está expirado, intentamos decodificarlo sin verificar la expiración
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM], options={"verify_exp": False})
        
        user_id = payload.get("user_id")
        nombre = payload.get("nombre")
        
        if not user_id or not nombre:
            return JSONResponse(
                status_code=401,
                content={
                    "detail": "Token inválido - datos de usuario faltantes",
                    "success": False
                }
            )
        
        # Verificar que el usuario aún existe en la base de datos
        existing_user = db.query(Usuario).filter(Usuario.IDUSUARIO == user_id).first()
        if not existing_user:
            return JSONResponse(
                status_code=401,
                content={
                    "detail": "Usuario no encontrado",
                    "success": False
                }
            )
        
        # Crear un nuevo token
        new_token = create_jwt_token(user_id, nombre)
        
        return JSONResponse(
            status_code=200,
            content={
                "detail": "Token refrescado exitosamente",
                "success": True,
                "token": new_token
            }
        )
        
    except jwt.InvalidTokenError:
        return JSONResponse(
            status_code=401,
            content={
                "detail": "Token inválido",
                "success": False
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "detail": f"Error al refrescar token: {str(e)}",
                "success": False
            }
        )

def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Security(HTTPBearer())):
    try:
        if not credentials:
            raise HTTPException(
                status_code=401,
                detail="No se encontraron credenciales de autenticación",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        token = credentials.credentials
        
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401,
                detail="Token expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.InvalidTokenError as e:
            raise HTTPException(
                status_code=401,
                detail=f"Token inválido: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Error de autenticación: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
