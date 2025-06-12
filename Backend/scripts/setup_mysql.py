#!/usr/bin/env python3
"""
Script para configurar MySQL
"""

import subprocess
import sys
import os

def install_dependencies():
    """Instalar dependencias de MySQL"""
    print("Instalando dependencias de MySQL...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "mysqlclient"])
        print("✓ mysqlclient instalado correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error instalando mysqlclient: {e}")
        print("Intentando con PyMySQL como alternativa...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "PyMySQL"])
            print("✓ PyMySQL instalado correctamente")
            return True
        except subprocess.CalledProcessError as e2:
            print(f"✗ Error instalando PyMySQL: {e2}")
            return False

def create_database():
    """Crear la base de datos LENDIT en MySQL"""
    print("Creando base de datos LENDIT...")
    
    # Intentar diferentes conectores MySQL
    mysql_connector = None
    
    try:
        import mysql.connector
        mysql_connector = 'mysql.connector'
    except ImportError:
        try:
            import pymysql
            mysql_connector = 'pymysql'
        except ImportError:
            print("✗ No se encontró ningún conector MySQL")
            print("Instalando mysql-connector-python...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "mysql-connector-python"])
                import mysql.connector
                mysql_connector = 'mysql.connector'
            except:
                print("✗ No se pudo instalar mysql-connector-python")
                return False
    
    try:
        if mysql_connector == 'mysql.connector':
            import mysql.connector
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root'
            )
        else:  # pymysql
            import pymysql
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='root',
                charset='utf8mb4'
            )
        
        cursor = conn.cursor()
        
        # Crear la base de datos si no existe
        cursor.execute("CREATE DATABASE IF NOT EXISTS LENDIT")
        cursor.execute("USE LENDIT")
        
        print("✓ Base de datos LENDIT creada correctamente")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"✗ Error creando base de datos: {e}")
        print("Asegúrate de que MySQL esté ejecutándose y las credenciales sean correctas")
        return False

def initialize_tables():
    """Inicializar tablas en MySQL"""
    print("Inicializando tablas en MySQL...")
    try:
        from entidades.baseDatos.init_mysql import init_mysql_db, create_default_data
        if init_mysql_db():
            print("✓ Tablas inicializadas correctamente")
            # Crear datos por defecto
            if create_default_data():
                print("✓ Datos por defecto creados")
            return True
        else:
            print("✗ Error inicializando tablas")
            return False
    except Exception as e:
        print(f"✗ Error inicializando tablas: {e}")
        return False

def main():
    """Función principal"""
    print("=== Configuración de MySQL para LENDIT ===\n")
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("entidades"):
        print("✗ Error: Ejecute este script desde el directorio Backend")
        return False
    
    # Paso 1: Instalar dependencias
    if not install_dependencies():
        print("✗ No se pudieron instalar las dependencias de MySQL")
        return False
    
    # Paso 2: Crear base de datos
    if not create_database():
        print("✗ No se pudo crear la base de datos")
        return False
    
    # Paso 3: Inicializar tablas
    if not initialize_tables():
        print("✗ No se pudieron inicializar las tablas")
        return False
    
    print("\n=== Configuración completada ===")
    print("✓ MySQL configurado correctamente")
    print("✓ Base de datos LENDIT lista para usar")
    print("\nPuede iniciar el servidor con: python main.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
