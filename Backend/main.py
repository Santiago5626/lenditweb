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

from entidades.baseDatos.db import init_db

app = FastAPI()

# Inicializar la base de datos
init_db()

# Orígenes permitidos (React corre en localhost:3000)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*", "Authorization", "Content-Type"],
    expose_headers=["*", "Authorization"],
)

app.include_router(login_router, prefix="/usuario")
app.include_router(solicitante_router, prefix="/solicitantes")
app.include_router(funcionesPrestamo, prefix="/prestamo")
app.include_router(producto_router, prefix="/productos")
