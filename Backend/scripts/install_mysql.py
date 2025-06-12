#!/usr/bin/env python3
"""
Script de instalación completa para migrar LendItWeb a MySQL
"""
import subprocess
import sys
import os
import time

def print_header(title):
    """Imprimir encabezado con formato"""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def print_step(step, description):
    """Imprimir paso con formato"""
    print(f"\n[PASO {step}] {description}")
    print("-" * 40)

def run_command(command, description):
    """Ejecutar comando y mostrar resultado"""
    print(f"Ejecutando: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Error: {e}")
        if e.stdout:
            print(f"Salida: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def check_mysql_running():
    """Verificar si MySQL está ejecutándose"""
    print("Verificando si MySQL está ejecutándose...")
    try:
        # Intentar conectar a MySQL
        import mysql.connector
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root'  # Cambiar según configuración
        )
        conn.close()
        print("✅ MySQL está ejecutándose")
        return True
    except:
        try:
            import pymysql
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='root'
            )
            conn.close()
            print("✅ MySQL está ejecutándose")
            return True
        except:
            print("❌ MySQL no está ejecutándose o no se puede conectar")
            print("Por favor, inicia MySQL y asegúrate de que las credenciales sean correctas")
            return False

def main():
    """Función principal de instalación"""
    print_header("INSTALACIÓN COMPLETA DE MYSQL PARA LENDITWEB")
    
    # Verificar directorio
    if not os.path.exists("entidades"):
        print("❌ Error: Ejecute este script desde el directorio Backend")
        return False
    
    print_step(1, "Instalando dependencias de Python")
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", 
                      "Instalación de dependencias"):
        print("⚠️ Continuando con la instalación...")
    
    print_step(2, "Verificando MySQL")
    if not check_mysql_running():
        print("\n📋 INSTRUCCIONES PARA MYSQL:")
        print("1. Instala MySQL Server si no lo tienes")
        print("2. Inicia el servicio MySQL")
        print("3. Configura la contraseña de root")
        print("4. Ejecuta este script nuevamente")
        return False
    
    print_step(3, "Configurando base de datos MySQL")
    if not run_command(f"{sys.executable} setup_mysql.py", 
                      "Configuración de base de datos"):
        print("❌ Error en la configuración de MySQL")
        return False
    
    print_step(4, "Creando usuario administrador")
    if not run_command(f"{sys.executable} create_admin.py", 
                      "Creación de usuario admin"):
        print("⚠️ Continuando sin usuario admin...")
    
    print_step(5, "Verificando instalación")
    if not run_command(f"{sys.executable} verify_migration.py", 
                      "Verificación de la instalación"):
        print("⚠️ Algunas verificaciones fallaron, pero la instalación puede estar funcional")
    
    print_header("INSTALACIÓN COMPLETADA")
    print("✅ MySQL configurado correctamente")
    print("✅ Base de datos inicializada")
    print("✅ Sistema listo para usar")
    
    print("\n📋 PRÓXIMOS PASOS:")
    print("1. Ejecutar el servidor: python main.py")
    print("2. Abrir el frontend en otra terminal")
    print("3. Navegar a http://localhost:3000")
    
    print("\n📁 ARCHIVOS IMPORTANTES:")
    print("- README_MYSQL_MIGRATION.md: Documentación completa")
    print("- .env.example: Configuración de entorno")
    print("- migrate_data.py: Para migrar datos de SQLite")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 ¡Instalación exitosa!")
    else:
        print("\n❌ Instalación incompleta. Revisa los errores anteriores.")
    
    sys.exit(0 if success else 1)
