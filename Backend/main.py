# main.py
from fastapi import FastAPI
from entidades.funciones.login import router as login_router
from entidades.funciones.estudiante import router as funcionesEstudiante
from entidades.funciones.prestamo import router as funcionesPrestamo

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Orígenes permitidos (React corre en localhost:3000)
origins = [
    "http://localhost:3000",
    # Puedes agregar más orígenes si lo necesitas
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # también puedes usar ["*"] para permitir todos (no recomendado en producción)
    allow_credentials=True,
    allow_methods=["*"],  # permite todos los métodos: GET, POST, etc.
    allow_headers=["*"],  # permite todos los headers
)


app.include_router(login_router, prefix="/usuario")
app.include_router(funcionesEstudiante, prefix="/estudiantes")
app.include_router(funcionesPrestamo, prefix="/prestamo")
    