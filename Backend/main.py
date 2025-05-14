# main.py
from fastapi import FastAPI
from entidades.funciones.login import router as login_router
from entidades.funciones.solicitante import router as solicitante_router
from entidades.funciones.prestamo import router as funcionesPrestamo
from entidades.funciones.producto_router import router as producto_router
from fastapi.middleware.cors import CORSMiddleware

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from init_db import init_database

app = FastAPI()

# Inicializar la base de datos y crear usuario admin si no existe
init_database()

# Orígenes permitidos (React corre en localhost:3000)
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # también puedes usar ["*"] para permitir todos (no recomendado en producción)
    allow_credentials=True,
    allow_methods=["*"],  # permite todos los métodos: GET, POST, etc.
    allow_headers=["*"],  # permite todos los headers
)

app.include_router(login_router, prefix="/usuario")
app.include_router(solicitante_router, prefix="/solicitantes")
app.include_router(funcionesPrestamo, prefix="/prestamo")
app.include_router(producto_router, prefix="/productos")
