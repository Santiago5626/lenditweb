from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import sqlite3
import os

# Obtener la ruta absoluta del archivo test.db en el directorio Backend
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATABASE_PATH = PROJECT_ROOT / "test.db"

print(f"Usando base de datos en: {DATABASE_PATH}")

# Configuración de la base de datos
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Configurar el engine con mejor manejo de conexiones
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
        "timeout": 60,
        "isolation_level": "IMMEDIATE"  # Mejor manejo de concurrencia
    },
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=20,  # Aumentar el tamaño del pool
    max_overflow=10,  # Permitir conexiones adicionales
    echo=True  # Habilitar logging de SQL
)

# Configurar logging
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Configurar la sesión con mejor manejo de concurrencia
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False  # Evitar problemas de expiración de objetos
)

def get_session():
    """Obtener una nueva sesión de base de datos"""
    session = SessionLocal()
    try:
        return session
    except:
        session.rollback()
        raise
    finally:
        session.close()

# Crear la clase base para los modelos
Base = declarative_base()

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA temp_store=MEMORY")
        cursor.execute("PRAGMA cache_size=10000")
        cursor.execute("PRAGMA busy_timeout=60000")  # Esperar hasta 60s en caso de bloqueo
        cursor.execute("PRAGMA journal_size_limit=67108864")  # Limitar tamaño del WAL a 64MB
        cursor.close()

def init_db():
    try:
        # Crear todas las tablas si no existen
        Base.metadata.create_all(bind=engine)
        print("Base de datos inicializada correctamente")
        return True
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
        return False

def reset_db():
    try:
        # Eliminar todas las tablas
        Base.metadata.drop_all(bind=engine)
        print("Tablas eliminadas correctamente")
        
        # Crear nuevamente las tablas
        Base.metadata.create_all(bind=engine)
        print("Tablas recreadas correctamente")
        return True
    except Exception as e:
        print(f"Error al reiniciar la base de datos: {e}")
        return False

# Función para obtener una sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
