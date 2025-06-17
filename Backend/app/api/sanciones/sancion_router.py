from fastapi import APIRouter
from .sancion import router as sancion_router

router = APIRouter()

# Incluir las rutas de sanciones
router.include_router(sancion_router, prefix="/sanciones", tags=["sanciones"])
