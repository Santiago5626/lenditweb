
# routers/login.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from entidades.modelos.usuario_modelo import Login, Usuario as UsuarioModel
from entidades.baseDatos.usuario import Usuario
from entidades.baseDatos.db import SessionLocal
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

from create_admin import create_admin_user

@router.post("/login")
async def login_user(user: Login, db: Session = Depends(get_db)):
    try:
        # Verificar si existen usuarios en la base de datos
        user_count = db.query(Usuario).count()
        if user_count == 0:
            # Si no hay usuarios, crear el admin
            create_admin_user()
            
        # Buscar el usuario por nombre o cc
        existing_user = db.query(Usuario).filter(
            (Usuario.nombre == user.nombre) | (Usuario.cc == user.nombre)
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
        if existing_user.password == user.password:
            token = create_jwt_token(existing_user.id, existing_user.nombre)
            return JSONResponse(
                status_code=200,
                content={
                    "detail": "Login exitoso",
                    "success": True,
                    "token": token,
                    "user": {
                        "nombre": existing_user.nombre,
                        "rol": existing_user.rol,
                        "cc": existing_user.cc
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
            (Usuario.cc == user.cc) | (Usuario.email == user.email)
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
            nombre=user.nombre,
            email=user.email,
            password=user.password,
            cc=user.cc,
            rol=user.rol,
            estado="1"
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
async def verify_token(authorization: str = Depends(lambda: None)):
    from fastapi import Request
    from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
    from fastapi import Security

    security = HTTPBearer()

    async def get_token(credentials: HTTPAuthorizationCredentials = Security(security)):
        return credentials.credentials

    token = await get_token()

    try:
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

from fastapi import Security, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    print("Verificando token JWT...")
    try:
        if not credentials:
            print("No se encontraron credenciales")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No se encontraron credenciales de autenticación",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        token = credentials.credentials
        print(f"Token recibido: {token[:10]}...")  # Solo mostramos los primeros 10 caracteres por seguridad
        
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            print("Token decodificado exitosamente")
            print(f"Payload: {payload}")
            return payload
        except jwt.ExpiredSignatureError:
            print("Token expirado")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.InvalidTokenError as e:
            print(f"Token inválido: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token inválido: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error de autenticación: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
