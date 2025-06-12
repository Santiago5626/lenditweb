from sqlalchemy import create_engine, event, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import mysql.connector
from mysql.connector import Error
import os

# Configuración de la base de datos MySQL
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"
MYSQL_DATABASE = "LENDIT"

def ensure_database_exists():
    """Crear la base de datos si no existe"""
    try:
        # Conectar a MySQL sin especificar base de datos
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            port=MYSQL_PORT
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Crear la base de datos si no existe
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE}")
            print(f"Base de datos {MYSQL_DATABASE} verificada/creada exitosamente")
            
            cursor.close()
            connection.close()
            return True
            
    except Error as e:
        print(f"Error al verificar/crear la base de datos: {e}")
        return False

# Asegurar que la base de datos existe antes de crear la URL de conexión
ensure_database_exists()

# URL de conexión a MySQL
DATABASE_URL = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

print(f"Conectando a MySQL: {MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}")

# Configurar el engine para MySQL
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=20,
    max_overflow=10,
    echo=False,
    connect_args={
        "charset": "utf8mb4",
        "autocommit": False
    }
)

# Configurar la sesión
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
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
def set_mysql_settings(dbapi_connection, connection_record):
    """Configurar ajustes específicos de MySQL"""
    with dbapi_connection.cursor() as cursor:
        cursor.execute("SET SESSION sql_mode='STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO'")
        cursor.execute("SET SESSION innodb_strict_mode=1")
        cursor.execute("SET SESSION foreign_key_checks=1")

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
