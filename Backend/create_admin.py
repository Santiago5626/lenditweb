from sqlalchemy.orm import Session
from entidades.baseDatos.db import SessionLocal, engine
from entidades.baseDatos.usuario import Usuario

def create_admin_user():
    print("Creando usuario administrador...")
    
    # Crear una sesión
    db = SessionLocal()
    
    try:
        # Verificar si el usuario admin ya existe
        existing_admin = db.query(Usuario).filter(Usuario.nombre == "Brian").first()
        
        if existing_admin:
            print("El usuario admin ya existe")
            return
        
        # Crear el usuario admin
        admin_user = Usuario(
            nombre="Brian",
            email="admin@example.com",
            password="admin",
            cc="1234",
            rol="administrador",
            estado="activo"
        )
        
        # Agregar y guardar en la base de datos
        db.add(admin_user)
        db.commit()
        print("Usuario admin creado exitosamente")
        
    except Exception as e:
        db.rollback()
        print(f"Error al crear usuario admin: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
