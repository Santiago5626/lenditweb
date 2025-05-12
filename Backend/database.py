from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///C:/Users/redol/OneDrive/Desktop/BaseDatos/test.db"

# Crea el engine de la base de datos
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Crea la sesión local para interactuar con la base de datos
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Crea la base de datos de clases de SQLAlchemy
Base = declarative_base()

# Dependencia para obtener la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
