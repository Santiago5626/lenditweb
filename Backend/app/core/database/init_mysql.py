from sqlalchemy import text
from .db import engine

def init_mysql_db():
    """Initialize MySQL database with all tables, triggers, views and indexes"""
    
    try:
        with engine.connect() as connection:
            # Create tables
            connection.execute(text("""
                -- 1. Tabla de tipos de productos
                CREATE TABLE IF NOT EXISTS GS_TIPO_PRODUCTO (
                    IDTIPOPRODUCTO INT AUTO_INCREMENT PRIMARY KEY,
                    NOMBRE_TIPO_PRODUCTO VARCHAR(60) NOT NULL UNIQUE
                );

                -- 2. Tabla de programas
                CREATE TABLE IF NOT EXISTS GS_PROGRAMA (
                    CODPROGRAMA VARCHAR(20) PRIMARY KEY,
                    NOMBRE_PROGRAMA VARCHAR(100) NOT NULL
                );

                -- 3. Tabla de fichas
                CREATE TABLE IF NOT EXISTS GS_FICHA (
                    CODFICHA VARCHAR(20) PRIMARY KEY,
                    CODPROGRAMA VARCHAR(20),
                    FECHA_INICIO DATE,
                    FECHA_FIN DATE,
                    CONSTRAINT fk_codprograma FOREIGN KEY (CODPROGRAMA) REFERENCES GS_PROGRAMA (CODPROGRAMA)
                );

                -- 4. Tabla de solicitantes
                CREATE TABLE IF NOT EXISTS GS_SOLICITANTE (
                    IDENTIFICACION VARCHAR(30) PRIMARY KEY,
                    PRIMER_NOMBRE VARCHAR(50) NOT NULL,
                    SEGUNDO_NOMBRE VARCHAR(50),
                    PRIMER_APELLIDO VARCHAR(50) NOT NULL,
                    SEGUNDO_APELLIDO VARCHAR(50),
                    CORREO VARCHAR(60),
                    TELEFONO VARCHAR(20),
                    ROL ENUM('aprendiz', 'contratista', 'funcionario', 'instructor') NOT NULL,
                    FICHA VARCHAR(20),
                    PROGRAMA VARCHAR(20),
                    ESTADO ENUM('apto', 'no apto') DEFAULT 'apto'
                );

                -- 5. Tabla de usuarios
                CREATE TABLE IF NOT EXISTS HS_USUARIO (
                    IDUSUARIO INT AUTO_INCREMENT PRIMARY KEY,
                    NOMBRE_USUARIO VARCHAR(255) NOT NULL UNIQUE,
                    CONTRASENA VARCHAR(255) NOT NULL,
                    ROL VARCHAR(50) NOT NULL
                );

                -- 6. Tabla de productos
                CREATE TABLE IF NOT EXISTS GS_PRODUCTO (
                    IDPRODUCTO INT AUTO_INCREMENT PRIMARY KEY,
                    CODIGO_INTERNO VARCHAR(100) NOT NULL UNIQUE,
                    NOMBRE VARCHAR(100) NOT NULL,
                    IDTIPOPRODUCTO INT NOT NULL,
                    PLACA_SENA VARCHAR(50),
                    SERIAL VARCHAR(100),
                    MARCA VARCHAR(60),
                    ESTADO VARCHAR(20) NOT NULL,
                    OBSERVACIONES TEXT,
                    CONSTRAINT FK_TIPO_PRODUCTO FOREIGN KEY (IDTIPOPRODUCTO) REFERENCES GS_TIPO_PRODUCTO(IDTIPOPRODUCTO)
                );

                -- 7. Solicitud de préstamo
                CREATE TABLE IF NOT EXISTS GS_SOLICITUD (
                    IDSOLICITUD INT AUTO_INCREMENT PRIMARY KEY,
                    IDENTIFICACION VARCHAR(30),
                    CODIGO_INTERNO VARCHAR(100),
                    FECHA_REGISTRO DATE,
                    ESTADO VARCHAR(20),
                    CONSTRAINT FK_IDENTIFICACION_SOLICITANTE FOREIGN KEY (IDENTIFICACION) REFERENCES GS_SOLICITANTE(IDENTIFICACION),
                    CONSTRAINT FK_CODIGO_INTERNO FOREIGN KEY (CODIGO_INTERNO) REFERENCES GS_PRODUCTO(CODIGO_INTERNO)
                );

                -- 8. Productos por solicitud
                CREATE TABLE IF NOT EXISTS GS_PRODUCTO_SOLICITUD (
                    IDPRODUCTOSOLICITUD INT AUTO_INCREMENT PRIMARY KEY,
                    CODIGO_INTERNO VARCHAR(100),
                    SOLICITUD_ID INT,
                    CONSTRAINT FK_CODIGO_INTERNO_PRODUCTO FOREIGN KEY (CODIGO_INTERNO) REFERENCES GS_PRODUCTO(CODIGO_INTERNO),
                    CONSTRAINT FK_SOLICITUD_PRODUCTO FOREIGN KEY (SOLICITUD_ID) REFERENCES GS_SOLICITUD(IDSOLICITUD)
                );

                -- 9. Tabla de préstamos
                CREATE TABLE IF NOT EXISTS GS_PRESTAMO (
                    IDPRESTAMO INT AUTO_INCREMENT PRIMARY KEY,
                    IDENTIFICACION_SOLICITANTE VARCHAR(30) NOT NULL,
                    IDPRODUCTO INT NOT NULL,
                    FECHA_INICIO DATETIME NOT NULL,
                    FECHA_FINAL DATETIME NOT NULL,
                    ESTADO ENUM('activo', 'rechazado', 'finalizado') DEFAULT 'activo',
                    OBSERVACIONES TEXT,
                    CONSTRAINT FK_SOLICITANTE_PRESTAMO FOREIGN KEY (IDENTIFICACION_SOLICITANTE) REFERENCES GS_SOLICITANTE(IDENTIFICACION),
                    CONSTRAINT FK_PRODUCTO_PRESTAMO FOREIGN KEY (IDPRODUCTO) REFERENCES GS_PRODUCTO(IDPRODUCTO)
                );

                -- 10. Tabla de sanciones
                CREATE TABLE IF NOT EXISTS GS_SANCION (
                    IDSANCION INT AUTO_INCREMENT PRIMARY KEY,
                    IDENTIFICACION VARCHAR(30) NOT NULL,
                    FECHA_SANCION DATETIME DEFAULT CURRENT_TIMESTAMP,
                    MOTIVO TEXT,
                    CONSTRAINT FK_IDTERCEROSANCION FOREIGN KEY (IDENTIFICACION) REFERENCES GS_SOLICITANTE(IDENTIFICACION)
                );

                -- 11. Tabla de trazabilidad
                CREATE TABLE IF NOT EXISTS GS_LOG_TRAZABILIDAD (
                    IDLOG INT AUTO_INCREMENT PRIMARY KEY,
                    IDUSUARIO INT NOT NULL,
                    FECHA TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ACCION VARCHAR(20) NOT NULL,
                    NOMBRE_TABLA VARCHAR(50) NOT NULL,
                    DATOS_ANTERIORES TEXT,
                    DATOS_NUEVOS TEXT,
                    CONSTRAINT FK_USUARIO_LOG FOREIGN KEY (IDUSUARIO) REFERENCES HS_USUARIO(IDUSUARIO)
                );

                -- 12. Conteo diario de inventario
                CREATE TABLE IF NOT EXISTS GS_CONTEO_DIARIO (
                    IDCONTEO INT AUTO_INCREMENT PRIMARY KEY,
                    FECHA DATE NOT NULL,
                    JORNADA ENUM('mañana', 'tarde') NOT NULL,
                    IDPRODUCTO INT NOT NULL,
                    CANTIDAD_DISPONIBLE INT NOT NULL,
                    CONSTRAINT FK_PRODUCTO_CONTEO FOREIGN KEY (IDPRODUCTO) REFERENCES GS_PRODUCTO(IDPRODUCTO)
                );
            """))

            connection.commit()
            print("✅ Tablas creadas correctamente")

            # Create indexes (sin IF NOT EXISTS para compatibilidad)
            try:
                indexes = [
                    "CREATE INDEX idx_estado_solicitante ON GS_SOLICITANTE(ESTADO)",
                    "CREATE INDEX idx_rol_solicitante ON GS_SOLICITANTE(ROL)",
                    "CREATE INDEX idx_estado_producto ON GS_PRODUCTO(ESTADO)",
                    "CREATE INDEX idx_tipo_producto ON GS_PRODUCTO(IDTIPOPRODUCTO)",
                    "CREATE INDEX idx_estado_solicitud ON GS_SOLICITUD(ESTADO)",
                    "CREATE INDEX idx_identificacion_solicitud ON GS_SOLICITUD(IDENTIFICACION)",
                    "CREATE INDEX idx_estado_prestamo ON GS_PRESTAMO(ESTADO)",
                    "CREATE INDEX idx_fecha_prestamo ON GS_PRESTAMO(FECHA_INICIO)",
                    "CREATE INDEX idx_identificacion_sancion ON GS_SANCION(IDENTIFICACION)",
                    "CREATE INDEX idx_fecha_conteo ON GS_CONTEO_DIARIO(FECHA)",
                    "CREATE INDEX idx_jornada_conteo ON GS_CONTEO_DIARIO(JORNADA)"
                ]
                
                for index_sql in indexes:
                    try:
                        connection.execute(text(index_sql))
                    except Exception as idx_error:
                        # Ignorar errores si el índice ya existe
                        if "Duplicate key name" not in str(idx_error):
                            print(f"⚠️ Advertencia creando índice: {idx_error}")
                
                connection.commit()
                print("✅ Índices creados correctamente")
                
            except Exception as e:
                print(f"⚠️ Advertencia con índices: {e}")

            print("✅ Base de datos MySQL inicializada correctamente")
            return True

    except Exception as e:
        print(f"❌ Error al inicializar la base de datos MySQL: {e}")
        return False

def create_default_data():
    """Create default data for the application"""
    try:
        with engine.connect() as connection:
            # Insert default product types
            default_types = [
                "equipo de cómputo",
                "cargador", 
                "mouse",
                "padmouse",
                "tarjeta micro SD",
                "guaya"
            ]
            
            for tipo in default_types:
                try:
                    connection.execute(text(
                        "INSERT IGNORE INTO GS_TIPO_PRODUCTO (NOMBRE_TIPO_PRODUCTO) VALUES (:tipo)"
                    ), {"tipo": tipo})
                except Exception as e:
                    # Ignorar si ya existe
                    pass
            
            connection.commit()
            print("✅ Datos por defecto creados")
            return True
            
    except Exception as e:
        print(f"⚠️ Error creando datos por defecto: {e}")
        return False

def migrate_data():
    """Migrate data from SQLite to MySQL"""
    # TODO: Implement data migration from SQLite to MySQL
    pass
