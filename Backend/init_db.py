from entidades.baseDatos.db import init_db, Base, engine
from entidades.baseDatos.usuario import Usuario
from entidades.baseDatos.solicitante import Solicitante

def init_database():
    print("Iniciando la creación de la base de datos...")
    
    try:
        # Crear todas las tablas
        Base.metadata.create_all(bind=engine)
        print("Tablas creadas exitosamente")
        
        # Crear usuario admin por defecto
        from sqlalchemy.orm import Session
        with Session(engine) as session:
            # Verificar si el usuario admin ya existe
            admin = session.query(Usuario).filter_by(nombre="admin").first()
            if not admin:
                admin = Usuario(
                    nombre="admin",
                    email="admin@example.com",
                    password="admin123",  # En producción usar hash
                    cc="admin",
                    rol="admin",
                    estado="activo"
                )
                session.add(admin)
                session.commit()
                print("Usuario admin creado exitosamente")
            else:
                print("El usuario admin ya existe")
                
    except Exception as e:
        print(f"Error durante la inicialización: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    init_database()
