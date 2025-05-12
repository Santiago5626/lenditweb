# routers/login.py
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from entidades.modelos.usuario_modelo import Login, Usuario as UsuarioModel   # Modelo Pydantic
from entidades.baseDatos.usuario import Usuario  # Modelo SQLAlchemy
from entidades.baseDatos.db import SessionLocal  # Función para obtener DB
 
router = APIRouter()

# Dependencia para obtener la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
async def login_user(user: Login, db: Session = Depends(get_db)):
    # Buscar el usuario por nombre
    existing_user = db.query(Usuario).filter(user.nombre == Usuario.nombre).first()

    # Verificar si el usuario existe
    if not existing_user:
        return JSONResponse(status_code=404, content={"detail": "Usuario no encontrado"})

    if existing_user.password == user.password:
        return JSONResponse(status_code=200, content={"detail": "Login exitoso"})
    else:
        return JSONResponse(status_code=401, content={"detail": "Contraseña incorrecta"})
    

@router.post("/registrar")
async def registrarUsuario(user: UsuarioModel, db: Session = Depends(get_db)):
    existing_user = db.query(Usuario).filter(user.cc == Usuario.cc).first()
    if existing_user:
                return JSONResponse(status_code=404, content={"detail": "ESTE USUARIO YA EXISTE"})

    if not existing_user:
        if user.cc == " ":
             cc = "admin"


        new_user= Usuario(
            nombre=user.nombre,
            email=user.email,
            password=user.password,
            cc=user.cc,
            rol=user.rol,
            estado=1,



    ) 
        try:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
        except Exception as e:
            db.rollback()
            return JSONResponse(status_code=500, content={"detail": f"Error al registrar: {str(e)}"})
