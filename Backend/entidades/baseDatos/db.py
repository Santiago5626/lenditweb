from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path  # Asegúrate de importar Path


BASE_DIR = Path(__file__).resolve().parent
DATABASE_URL = f"sqlite:///{BASE_DIR}/test.db"


engine = create_engine(DATABASE_URL  , connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False,autoflush=False)
Base= declarative_base()



