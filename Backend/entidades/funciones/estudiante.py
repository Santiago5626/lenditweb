from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from entidades.modelos.estudiante_modelo import Estudiante as estudianteModel, Eliminar   # Modelo Pydantic
from entidades.baseDatos.estudiante import Estudiante  # Modelo SQLAlchemy
from entidades.baseDatos.db import SessionLocal  # Función para obtener DB
 

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.get("/obtener")
async def getEstudiantes(db: Session = Depends(get_db)):
    estudiantes = db.query(Estudiante).all()

    if not estudiantes:
        return JSONResponse(status_code=404, content={"detail": "No hay usuarios registrados"})
    
    return estudiantes




@router.post("/registrar")
async def registrarUsuario(estudiante: estudianteModel, db: Session = Depends(get_db)):
    existing_user = db.query(Estudiante).filter(estudiante.cc == Estudiante.cc).first()
    if existing_user:
                return JSONResponse(status_code=404, content={"detail": "ESTE ESTUDIANTE YA EXISTE"})

    if not existing_user:
 

        nuevo_estudiante= Estudiante(
            cc=estudiante.cc,
            apellido=estudiante.apellido,
            nombre=estudiante.nombre,
            email=estudiante.email,
           


    ) 
        try:
            

            db.add(nuevo_estudiante)
            db.commit()
            db.refresh(nuevo_estudiante)
            return JSONResponse(status_code=404, content={"detail": "Estudiante Registrado"})

        except Exception as e:
            db.rollback()
            return JSONResponse(status_code=500, content={"detail": f"Error al registrar: {str(e)}"})
        


@router.put("/actualizar")
async def registrarUsuario(estudiante: estudianteModel, db: Session = Depends(get_db)):
 # Buscar al estudiante por su cédula
    existing_user = db.query(Estudiante).filter(Estudiante.cc == estudiante.cc).first()

    if existing_user:
        # Actualizar el estudiante directamente en la base de datos
        db.query(Estudiante).filter(Estudiante.cc == estudiante.cc).update({
            Estudiante.nombre: estudiante.nombre,
            Estudiante.email: estudiante.email
            # Agrega más campos que quieras actualizar
        })
        db.commit()  # Guardar cambios
        return JSONResponse(status_code=200, content={"detail": "Estudiante Actualizado"})
    else:
        return JSONResponse(status_code=404, content={"detail": "Estudiante No Encontrado"})
  

@router.delete("/eliminar")
async def registrarUsuario(estudiante: Eliminar, db: Session = Depends(get_db)):
    existing_user = db.query(Estudiante).filter(estudiante.cc == Estudiante.cc).first()
    if existing_user:
                
                try:
                    db.query(Estudiante).filter(Estudiante.cc == estudiante.cc).delete()
                    db.commit()
                    return JSONResponse(status_code=200, content={"detail": "Estudiante Eliminado"})
                except Exception as e:
                       db.rollback()
                       return JSONResponse(status_code=500, content={"detail": f"Error al eliminar: {str(e)}"})

    if not existing_user:
                         return JSONResponse(status_code=404, content={"detail": "Estudiante No Existe"})

 