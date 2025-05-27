from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from entidades.modelos.prestamo_modelo import Prestamo as prestamomodel, ActualizarEstado, buscar  # Modelo Pydantic
from entidades.baseDatos.prestamo import Prestamo  # Modelo SQLAlchemy
from entidades.baseDatos.db import SessionLocal  # Función para obtener DB
 


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.get("/obtener")
async def obtenerPrestamos(db: Session = Depends(get_db)):
    prestamo = db.query(Prestamo).all()

    if not Prestamo:
        return JSONResponse(status_code=404, content={"detail": "No hay usuarios registrados"})
    
    return prestamo

@router.post("/Solicitar")
async def registrarUsuario(prestamo: prestamomodel, db: Session = Depends(get_db)):
     

        nuevo_prestamo= Prestamo(
                identificacion_solicitante=prestamo.identificacion_solicitante,
                idProducto=prestamo.idProducto,
                fechaFinal=prestamo.fechaFinal,
                estado=0


    ) 
        try:
            db.add(nuevo_prestamo)
            db.commit()
            db.refresh(nuevo_prestamo)
            return JSONResponse(status_code=404, content={"detail": "Prestamo Solicitado"})

        except Exception as e:
            db.rollback()
            return JSONResponse(status_code=500, content={"detail": f"Error al Solicitar: {str(e)}"})
        



@router.put("/actualizarEstado")
async def registrarUsuario(prestamo: ActualizarEstado, db: Session = Depends(get_db)):
 # Buscar el prestamo por su id
    existing_user = db.query(Prestamo).filter(prestamo.id == Prestamo.id).first()

    if existing_user:
        # Actualizar el estado del prestamo solicitado directamente en la base de datos
        db.query(Prestamo).filter(Prestamo.id == prestamo.id).update({
            Prestamo.estado: prestamo.estado
            # Agrega más campos que quieras actualizar
        })
        db.commit()  # Guardar cambios
        if prestamo.estado==1:
         return JSONResponse(status_code=200, content={"detail": "Prestamo Autorizado"})
        elif prestamo.estado==2:
             return JSONResponse(status_code=200, content={"detail": "Prestamo NO Autorizado"})

    
    else:
        return JSONResponse(status_code=404, content={"detail": "Prestamo No Encontrado"})
  

@router.delete("/eliminar")
async def registrarUsuario(prestamo: buscar, db: Session = Depends(get_db)):
    existing_user = db.query(Prestamo).filter(prestamo.id == Prestamo.id).first()
    if existing_user:
                
                try:
                    db.query(Prestamo).filter(Prestamo.id == prestamo.id).delete()
                    db.commit()
                    return JSONResponse(status_code=200, content={"detail": "Prestamo Eliminado"})
                except Exception as e:
                       db.rollback()
                       return JSONResponse(status_code=500, content={"detail": f"Error al eliminar: {str(e)}"})

    if not existing_user:
                         return JSONResponse(status_code=404, content={"detail": "Prestamo No Existe"})


@router.get("/buscar")
async def buscarPrestamo(id: str = None, db: Session = Depends(get_db)):
    query = db.query(Prestamo)
    if id:
        query = query.filter(Prestamo.id == id)
    
    prestamos = query.all()  # Ejecutamos la consulta

    if not prestamos:
        return JSONResponse(status_code=404, content={"detail": "No se encontraron préstamos"})
    
    return prestamos
