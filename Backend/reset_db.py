from entidades.baseDatos.db import reset_db

def main():
    print("Iniciando reinicio de la base de datos...")
    if reset_db():
        print("Base de datos reiniciada exitosamente")
    else:
        print("Error al reiniciar la base de datos")

if __name__ == "__main__":
    main()
