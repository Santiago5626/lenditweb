# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Agregar el directorio app al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Importar configuración
from app.core.config.settings import settings

# Importar routers desde la nueva estructura
from app.api.auth.login import router as login_router
from app.api.solicitantes.solicitante import router as solicitante_router
from app.api.prestamos.prestamo import router as funcionesPrestamo
from app.api.productos.producto_router import router as producto_router
from app.api.productos.tipo_producto_router import router as tipo_producto_router
from app.api.solicitudes.solicitud import router as solicitud_router
from app.api.sanciones.sancion_router import router as sancion_router

# Importar configuración de base de datos
from app.core.database.db import init_db, get_db

# Importar todos los modelos para asegurar que estén registrados con SQLAlchemy
from app.core.database.producto import Producto
from app.core.database.tipo_producto import TipoProducto
from app.core.database.solicitante import Solicitante
from app.core.database.usuario import Usuario
from app.core.database.prestamo import Prestamo
from app.core.database.programas import Programas
from app.core.database.ficha import Ficha
from app.core.database.solicitud import Solicitud
from app.core.database.producto_solicitud import ProductoSolicitud
from app.core.database.sancion import Sancion
from app.core.database.log_trazabilidad import LogTrazabilidad
from app.core.database.conteo_diario import ConteoDiario

app = FastAPI(title=settings.PROJECT_NAME)

# Inicializar la base de datos
init_db()

# Inicializar tipos de producto por defecto
from app.api.productos.tipo_producto import init_tipos_producto
db = next(get_db())
try:
    init_tipos_producto(db)
except Exception as e:
    print(f"Error al inicializar tipos de producto: {e}")
finally:
    db.close()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*", "Authorization", "Content-Type"],
    expose_headers=["*", "Authorization"],
)

# Rutas de la API
app.include_router(login_router, prefix="/usuario", tags=["Usuarios"])
app.include_router(solicitante_router, prefix="/solicitantes", tags=["Solicitantes"])
app.include_router(funcionesPrestamo, prefix="/prestamo", tags=["Préstamos"])
app.include_router(producto_router, prefix="/productos", tags=["Productos"])
app.include_router(tipo_producto_router, prefix="/tipos-producto", tags=["Tipos de Producto"])
app.include_router(solicitud_router, prefix="/solicitudes", tags=["Solicitudes"])
app.include_router(sancion_router, prefix="/api", tags=["Sanciones"])

@app.get("/")
async def root():
    return {"message": "API de Gestión de Préstamos"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
