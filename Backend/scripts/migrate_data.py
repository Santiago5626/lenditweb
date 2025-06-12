#!/usr/bin/env python3
"""
Script para migrar datos de SQLite a MySQL
"""
import os
import sys
import sqlite3
try:
    import mysql.connector
    MYSQL_CONNECTOR_AVAILABLE = True
except ImportError:
    try:
        import pymysql
        MYSQL_CONNECTOR_AVAILABLE = False
    except ImportError:
        print("Error: Necesitas instalar mysql-connector-python o pymysql")
        print("Ejecuta: pip install mysql-connector-python")
        sys.exit(1)
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuración de bases de datos
SQLITE_DB = "lenditweb.db"  # Ajustar ruta si es necesario
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'lenditweb_user',
    'password': 'lenditweb_password',
    'database': 'lenditweb_db',
    'charset': 'utf8mb4'
}

def connect_sqlite():
    """Conectar a SQLite"""
    if not os.path.exists(SQLITE_DB):
        logger.error(f"Base de datos SQLite no encontrada: {SQLITE_DB}")
        return None
    
    try:
        conn = sqlite3.connect(SQLITE_DB)
        conn.row_factory = sqlite3.Row  # Para acceder por nombre de columna
        logger.info("Conectado a SQLite exitosamente")
        return conn
    except Exception as e:
        logger.error(f"Error conectando a SQLite: {e}")
        return None

def connect_mysql():
    """Conectar a MySQL"""
    try:
        if MYSQL_CONNECTOR_AVAILABLE:
            conn = mysql.connector.connect(**MYSQL_CONFIG)
        else:
            conn = pymysql.connect(**MYSQL_CONFIG)
        logger.info("Conectado a MySQL exitosamente")
        return conn
    except Exception as e:
        logger.error(f"Error conectando a MySQL: {e}")
        return None

def migrate_solicitantes(sqlite_conn, mysql_conn):
    """Migrar tabla solicitantes"""
    logger.info("Migrando solicitantes...")
    
    sqlite_cursor = sqlite_conn.cursor()
    mysql_cursor = mysql_conn.cursor()
    
    try:
        # Obtener datos de SQLite
        sqlite_cursor.execute("SELECT * FROM solicitantes")
        rows = sqlite_cursor.fetchall()
        
        migrated = 0
        errors = 0
        
        for row in rows:
            try:
                # Mapear datos al nuevo esquema
                insert_query = """
                INSERT INTO GS_SOLICITANTE (
                    identificacion, primer_nombre, segundo_nombre, primer_apellido, 
                    segundo_apellido, correo, telefono, rol, ficha, programa, estado
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                values = (
                    row['identificacion'],
                    row['primer_nombre'],
                    row['segundo_nombre'],
                    row['primer_apellido'],
                    row['segundo_apellido'],
                    row['correo'],
                    row['telefono'],
                    row['rol'],
                    row['ficha'],
                    row['programa'],
                    'apto'  # Estado por defecto
                )
                
                mysql_cursor.execute(insert_query, values)
                migrated += 1
                
            except Exception as e:
                logger.error(f"Error migrando solicitante {row['identificacion']}: {e}")
                errors += 1
        
        mysql_conn.commit()
        logger.info(f"Solicitantes migrados: {migrated}, errores: {errors}")
        
    except Exception as e:
        logger.error(f"Error en migración de solicitantes: {e}")
        mysql_conn.rollback()

def migrate_tipos_producto(sqlite_conn, mysql_conn):
    """Migrar tabla tipos de producto"""
    logger.info("Migrando tipos de producto...")
    
    sqlite_cursor = sqlite_conn.cursor()
    mysql_cursor = mysql_conn.cursor()
    
    try:
        # Obtener datos de SQLite
        sqlite_cursor.execute("SELECT * FROM tipos_producto")
        rows = sqlite_cursor.fetchall()
        
        migrated = 0
        errors = 0
        
        for row in rows:
            try:
                insert_query = """
                INSERT INTO GS_TIPO_PRODUCTO (NOMBRE_TIPO_PRODUCTO) 
                VALUES (%s)
                """
                
                mysql_cursor.execute(insert_query, (row['nombre'],))
                migrated += 1
                
            except Exception as e:
                logger.error(f"Error migrando tipo producto {row['nombre']}: {e}")
                errors += 1
        
        mysql_conn.commit()
        logger.info(f"Tipos de producto migrados: {migrated}, errores: {errors}")
        
    except Exception as e:
        logger.error(f"Error en migración de tipos de producto: {e}")
        mysql_conn.rollback()

def migrate_productos(sqlite_conn, mysql_conn):
    """Migrar tabla productos"""
    logger.info("Migrando productos...")
    
    sqlite_cursor = sqlite_conn.cursor()
    mysql_cursor = mysql_conn.cursor()
    
    try:
        # Obtener datos de SQLite
        sqlite_cursor.execute("SELECT * FROM productos")
        rows = sqlite_cursor.fetchall()
        
        migrated = 0
        errors = 0
        
        for row in rows:
            try:
                insert_query = """
                INSERT INTO GS_PRODUCTO (
                    CODIGO_INTERNO, NOMBRE, IDTIPOPRODUCTO, PLACA_SENA, 
                    SERIAL, MARCA, ESTADO, OBSERVACIONES
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                values = (
                    row['codigoInterno'],
                    row['nombre'],
                    row['idTipoProducto'],
                    row['placaSena'],
                    row['serial'],
                    row['marca'],
                    row['estado'],
                    row['observaciones']
                )
                
                mysql_cursor.execute(insert_query, values)
                migrated += 1
                
            except Exception as e:
                logger.error(f"Error migrando producto {row['codigoInterno']}: {e}")
                errors += 1
        
        mysql_conn.commit()
        logger.info(f"Productos migrados: {migrated}, errores: {errors}")
        
    except Exception as e:
        logger.error(f"Error en migración de productos: {e}")
        mysql_conn.rollback()

def migrate_usuarios(sqlite_conn, mysql_conn):
    """Migrar tabla usuarios"""
    logger.info("Migrando usuarios...")
    
    sqlite_cursor = sqlite_conn.cursor()
    mysql_cursor = mysql_conn.cursor()
    
    try:
        # Obtener datos de SQLite
        sqlite_cursor.execute("SELECT * FROM usuarios")
        rows = sqlite_cursor.fetchall()
        
        migrated = 0
        errors = 0
        
        for row in rows:
            try:
                insert_query = """
                INSERT INTO HS_USUARIO (NOMBRE_USUARIO, CONTRASENA, ROL) 
                VALUES (%s, %s, %s)
                """
                
                values = (
                    row['nombreUsuario'],
                    row['contrasena'],
                    row['rol']
                )
                
                mysql_cursor.execute(insert_query, values)
                migrated += 1
                
            except Exception as e:
                logger.error(f"Error migrando usuario {row['nombreUsuario']}: {e}")
                errors += 1
        
        mysql_conn.commit()
        logger.info(f"Usuarios migrados: {migrated}, errores: {errors}")
        
    except Exception as e:
        logger.error(f"Error en migración de usuarios: {e}")
        mysql_conn.rollback()

def migrate_prestamos(sqlite_conn, mysql_conn):
    """Migrar tabla préstamos"""
    logger.info("Migrando préstamos...")
    
    sqlite_cursor = sqlite_conn.cursor()
    mysql_cursor = mysql_conn.cursor()
    
    try:
        # Obtener datos de SQLite
        sqlite_cursor.execute("SELECT * FROM prestamos")
        rows = sqlite_cursor.fetchall()
        
        migrated = 0
        errors = 0
        
        for row in rows:
            try:
                # Mapear estados numéricos a strings
                estado_map = {1: 'activo', 2: 'rechazado', 3: 'finalizado'}
                estado = estado_map.get(row['estado'], 'activo')
                
                insert_query = """
                INSERT INTO GS_PRESTAMO (
                    IDENTIFICACION_SOLICITANTE, IDPRODUCTO, FECHA_INICIO, 
                    FECHA_FINAL, ESTADO, OBSERVACIONES
                ) VALUES (%s, %s, %s, %s, %s, %s)
                """
                
                values = (
                    row['identificacionSolicitante'],
                    row['idProducto'],
                    datetime.now(),  # Fecha inicio por defecto
                    row['fechaFinal'],
                    estado,
                    None  # Observaciones por defecto
                )
                
                mysql_cursor.execute(insert_query, values)
                migrated += 1
                
            except Exception as e:
                logger.error(f"Error migrando préstamo ID {row['id']}: {e}")
                errors += 1
        
        mysql_conn.commit()
        logger.info(f"Préstamos migrados: {migrated}, errores: {errors}")
        
    except Exception as e:
        logger.error(f"Error en migración de préstamos: {e}")
        mysql_conn.rollback()

def main():
    """Función principal de migración"""
    logger.info("Iniciando migración de SQLite a MySQL...")
    
    # Conectar a las bases de datos
    sqlite_conn = connect_sqlite()
    if not sqlite_conn:
        return False
    
    mysql_conn = connect_mysql()
    if not mysql_conn:
        sqlite_conn.close()
        return False
    
    try:
        # Ejecutar migraciones en orden
        migrate_tipos_producto(sqlite_conn, mysql_conn)
        migrate_solicitantes(sqlite_conn, mysql_conn)
        migrate_productos(sqlite_conn, mysql_conn)
        migrate_usuarios(sqlite_conn, mysql_conn)
        migrate_prestamos(sqlite_conn, mysql_conn)
        
        logger.info("Migración completada exitosamente!")
        return True
        
    except Exception as e:
        logger.error(f"Error durante la migración: {e}")
        return False
        
    finally:
        sqlite_conn.close()
        mysql_conn.close()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
