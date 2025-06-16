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
                CREATE TABLE IF NOT EXISTS GS_PROGRAMAS (
                    CODPROGRAMA VARCHAR(20) PRIMARY KEY,
                    NOMBRE_PROGRAMA VARCHAR(100) NOT NULL
                );

                -- 3. Tabla de fichas
                CREATE TABLE IF NOT EXISTS GS_FICHA (
                    CODFICHA VARCHAR(20) PRIMARY KEY,
                    CODPROGRAMA VARCHAR(20),
                    FECHA_INICIO DATE,
                    FECHA_FIN DATE,
                    CONSTRAINT fk_codprograma FOREIGN KEY (CODPROGRAMA) REFERENCES GS_PROGRAMAS(CODPROGRAMA)
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
                    ESTADO ENUM('apto', 'no apto') DEFAULT 'apto',
                    CONSTRAINT FK_FICHA_SOLICITANTE FOREIGN KEY (FICHA) REFERENCES GS_FICHA(CODFICHA),
                    CONSTRAINT FK_PROGRAMA_SOLICITANTE FOREIGN KEY (PROGRAMA) REFERENCES GS_PROGRAMAS(CODPROGRAMA)
                );

                -- 5. Tabla de productos
                CREATE TABLE IF NOT EXISTS GS_PRODUCTO (
                    IDPRODUCTO INT AUTO_INCREMENT PRIMARY KEY,
                    CODIGO_INTERNO VARCHAR(100) NOT NULL UNIQUE,
                    NOMBRE VARCHAR(100) NOT NULL,
                    IDTIPOPRODUCTO INT NOT NULL,
                    PLACA_SENA VARCHAR(50),
                    SERIAL VARCHAR(100),
                    MARCA VARCHAR(60),
                    ESTADO ENUM('disponible', 'prestado', 'mantenimiento', 'dado de baja') DEFAULT 'disponible',
                    OBSERVACIONES TEXT,
                    CONSTRAINT FK_TIPO_PRODUCTO FOREIGN KEY (IDTIPOPRODUCTO) REFERENCES GS_TIPO_PRODUCTO(IDTIPOPRODUCTO)
                );

                -- 6. Tabla de solicitudes
                CREATE TABLE IF NOT EXISTS GS_SOLICITUD (
                    IDSOLICITUD INT AUTO_INCREMENT PRIMARY KEY,
                    IDENTIFICACION VARCHAR(30) NOT NULL,
                    FECHA_REGISTRO DATETIME DEFAULT CURRENT_TIMESTAMP,
                    ESTADO ENUM('pendiente', 'aprobado', 'rechazado', 'finalizado') DEFAULT 'pendiente',
                    OBSERVACIONES TEXT,
                    CONSTRAINT FK_SOLICITANTE_SOLICITUD FOREIGN KEY (IDENTIFICACION) REFERENCES GS_SOLICITANTE(IDENTIFICACION)
                );

                -- 7. Tabla de productos por solicitud
                CREATE TABLE IF NOT EXISTS GS_PRODUCTO_SOLICITUD (
                    PRODUCTO_ID INT,
                    SOLICITUD_ID INT,
                    PRIMARY KEY (PRODUCTO_ID, SOLICITUD_ID),
                    CONSTRAINT FK_PRODUCTO_SOLICITUD FOREIGN KEY (PRODUCTO_ID) REFERENCES GS_PRODUCTO(IDPRODUCTO),
                    CONSTRAINT FK_SOLICITUD_PRODUCTO FOREIGN KEY (SOLICITUD_ID) REFERENCES GS_SOLICITUD(IDSOLICITUD)
                );

                -- 8. Tabla de préstamos
                CREATE TABLE IF NOT EXISTS HS_PRESTAMO (
                    IDPRESTAMO INT AUTO_INCREMENT PRIMARY KEY,
                    IDSOLICITUD INT,
                    FECHA_REGISTRO DATE,
                    FECHA_LIMITE DATE,
                    FECHA_PROLONGACION DATE,
                    CONSTRAINT FK_SOLICITUD_PRESTAMO FOREIGN KEY (IDSOLICITUD) REFERENCES GS_SOLICITUD(IDSOLICITUD)
                );

                -- 9. Tabla de usuarios
                CREATE TABLE IF NOT EXISTS GS_USUARIO (
                    IDUSUARIO INT AUTO_INCREMENT PRIMARY KEY,
                    NOMBRE_USUARIO VARCHAR(255) NOT NULL UNIQUE,
                    CONTRASENA VARCHAR(255) NOT NULL,
                    ROL ENUM('admin', 'funcionario') NOT NULL DEFAULT 'funcionario'
                );

                -- 10. Tabla de log de trazabilidad
                CREATE TABLE IF NOT EXISTS GS_LOG_TRAZABILIDAD (
                    IDLOG INT AUTO_INCREMENT PRIMARY KEY,
                    IDUSUARIO INT,
                    FECHA TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ACCION VARCHAR(20) NOT NULL,
                    NOMBRE_TABLA VARCHAR(50) NOT NULL,
                    DATOS_ANTERIORES TEXT,
                    DATOS_NUEVOS TEXT,
                    CONSTRAINT FK_USUARIO_LOG FOREIGN KEY (IDUSUARIO) REFERENCES GS_USUARIO(IDUSUARIO)
                );
            """))

            # Create triggers
            connection.execute(text("""
                -- Trigger para actualizar estado del producto al crear préstamo
                DELIMITER //
                CREATE TRIGGER IF NOT EXISTS after_prestamo_insert
                AFTER INSERT ON HS_PRESTAMO
                FOR EACH ROW
                BEGIN
                    UPDATE GS_PRODUCTO p
                    INNER JOIN GS_PRODUCTO_SOLICITUD ps ON p.IDPRODUCTO = ps.PRODUCTO_ID
                    WHERE ps.SOLICITUD_ID = NEW.IDSOLICITUD
                    SET p.ESTADO = 'prestado';
                END //
                DELIMITER ;

                -- Trigger para actualizar estado del producto al devolver préstamo
                DELIMITER //
                CREATE TRIGGER IF NOT EXISTS after_prestamo_devolucion
                AFTER UPDATE ON HS_PRESTAMO
                FOR EACH ROW
                BEGIN
                    IF NEW.FECHA_DEVOLUCION IS NOT NULL AND OLD.FECHA_DEVOLUCION IS NULL THEN
                        UPDATE GS_PRODUCTO p
                        INNER JOIN GS_PRODUCTO_SOLICITUD ps ON p.IDPRODUCTO = ps.PRODUCTO_ID
                        WHERE ps.SOLICITUD_ID = NEW.IDSOLICITUD
                        SET p.ESTADO = 'disponible';
                        
                        UPDATE GS_SOLICITUD
                        SET ESTADO = 'finalizado'
                        WHERE IDSOLICITUD = NEW.IDSOLICITUD;
                    END IF;
                END //
                DELIMITER ;

                -- Trigger para validar fechas de préstamo
                DELIMITER //
                CREATE TRIGGER IF NOT EXISTS before_prestamo_insert
                BEFORE INSERT ON HS_PRESTAMO
                FOR EACH ROW
                BEGIN
                    IF NEW.FECHA_LIMITE <= NEW.FECHA_REGISTRO THEN
                        SIGNAL SQLSTATE '45000'
                        SET MESSAGE_TEXT = 'La fecha límite debe ser posterior a la fecha de registro';
                    END IF;
                END //
                DELIMITER ;

                -- Trigger para validar prolongación
                DELIMITER //
                CREATE TRIGGER IF NOT EXISTS before_prestamo_update
                BEFORE UPDATE ON HS_PRESTAMO
                FOR EACH ROW
                BEGIN
                    IF NEW.FECHA_PROLONGACION IS NOT NULL AND OLD.FECHA_PROLONGACION IS NULL THEN
                        IF NEW.FECHA_PROLONGACION <= OLD.FECHA_LIMITE THEN
                            SIGNAL SQLSTATE '45000'
                            SET MESSAGE_TEXT = 'La fecha de prolongación debe ser posterior a la fecha límite actual';
                        END IF;
                    END IF;
                END //
                DELIMITER ;
            """))

            # Create indexes
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_estado_solicitante ON GS_SOLICITANTE(ESTADO)",
                "CREATE INDEX IF NOT EXISTS idx_rol_solicitante ON GS_SOLICITANTE(ROL)",
                "CREATE INDEX IF NOT EXISTS idx_estado_producto ON GS_PRODUCTO(ESTADO)",
                "CREATE INDEX IF NOT EXISTS idx_estado_solicitud ON GS_SOLICITUD(ESTADO)",
                "CREATE INDEX IF NOT EXISTS idx_fecha_prestamo ON HS_PRESTAMO(FECHA_REGISTRO)",
                "CREATE INDEX IF NOT EXISTS idx_fecha_limite ON HS_PRESTAMO(FECHA_LIMITE)",
                "CREATE INDEX IF NOT EXISTS idx_fecha_prolongacion ON HS_PRESTAMO(FECHA_PROLONGACION)"
            ]
            
            for index_sql in indexes:
                try:
                    connection.execute(text(index_sql))
                except Exception as idx_error:
                    if "Duplicate key name" not in str(idx_error):
                        print(f"⚠️ Advertencia creando índice: {idx_error}")

            connection.commit()
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
                "Equipo de cómputo",
                "Cargador", 
                "Mouse",
                "Padmouse",
                "Tarjeta micro SD",
                "Guaya",
                "Cable HDMI",
                "Cable VGA",
                "Adaptador",
                "Otro"
            ]
            
            for tipo in default_types:
                try:
                    connection.execute(text(
                        "INSERT IGNORE INTO GS_TIPO_PRODUCTO (NOMBRE_TIPO_PRODUCTO) VALUES (:tipo)"
                    ), {"tipo": tipo})
                except Exception as e:
                    pass
            
            connection.commit()
            print("✅ Datos por defecto creados")
            return True
            
    except Exception as e:
        print(f"⚠️ Error creando datos por defecto: {e}")
        return False
