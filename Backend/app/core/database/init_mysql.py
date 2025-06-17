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
                    ESTADO ENUM('Disponible', 'Prestado', 'Mantenimiento', 'Dado de baja') DEFAULT 'Disponible',
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

                -- 11. Tabla de sanciones
                CREATE TABLE IF NOT EXISTS GS_SANCION (
                    IDSANCION INT AUTO_INCREMENT PRIMARY KEY,
                    IDENTIFICACION VARCHAR(30) NOT NULL,
                    IDPRESTAMO INT NOT NULL,
                    FECHA_INICIO DATE NOT NULL,
                    FECHA_FIN DATE NOT NULL,
                    DIAS_SANCION INT NOT NULL DEFAULT 3,
                    MOTIVO VARCHAR(255) NOT NULL DEFAULT 'Entrega tardía de préstamo',
                    ESTADO ENUM('activa', 'cumplida', 'cancelada') NOT NULL DEFAULT 'activa',
                    FECHA_REGISTRO DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT FK_SANCION_SOLICITANTE FOREIGN KEY (IDENTIFICACION) REFERENCES GS_SOLICITANTE(IDENTIFICACION),
                    CONSTRAINT FK_SANCION_PRESTAMO FOREIGN KEY (IDPRESTAMO) REFERENCES HS_PRESTAMO(IDPRESTAMO)
                );
            """))

            # Create triggers - Drop and recreate to ensure they are updated
            triggers = [
                # Trigger para actualizar estado del producto al crear préstamo
                "DROP TRIGGER IF EXISTS after_prestamo_insert",
                """
                CREATE TRIGGER after_prestamo_insert
                AFTER INSERT ON HS_PRESTAMO
                FOR EACH ROW
                BEGIN
                    UPDATE GS_PRODUCTO p
                    INNER JOIN GS_PRODUCTO_SOLICITUD ps ON p.IDPRODUCTO = ps.PRODUCTO_ID
                    WHERE ps.SOLICITUD_ID = NEW.IDSOLICITUD
                    SET p.ESTADO = 'Prestado';
                END
                """,
                
                # Trigger para actualizar estado del producto al finalizar solicitud
                "DROP TRIGGER IF EXISTS after_solicitud_finalizada",
                """
                CREATE TRIGGER after_solicitud_finalizada
                AFTER UPDATE ON GS_SOLICITUD
                FOR EACH ROW
                BEGIN
                    IF NEW.ESTADO = 'finalizado' AND OLD.ESTADO != 'finalizado' THEN
                        UPDATE GS_PRODUCTO p
                        INNER JOIN GS_PRODUCTO_SOLICITUD ps ON p.IDPRODUCTO = ps.PRODUCTO_ID
                        WHERE ps.SOLICITUD_ID = NEW.IDSOLICITUD
                        SET p.ESTADO = 'Disponible';
                    END IF;
                END
                """,
                
                # Trigger para validar fechas de préstamo
                "DROP TRIGGER IF EXISTS before_prestamo_insert",
                """
                CREATE TRIGGER before_prestamo_insert
                BEFORE INSERT ON HS_PRESTAMO
                FOR EACH ROW
                BEGIN
                    IF NEW.FECHA_LIMITE <= NEW.FECHA_REGISTRO THEN
                        SIGNAL SQLSTATE '45000'
                        SET MESSAGE_TEXT = 'La fecha límite debe ser posterior a la fecha de registro';
                    END IF;
                END
                """,
                
                # Trigger para sancionar préstamos vencidos
                "DROP TRIGGER IF EXISTS tr_sancionar_prestamo_vencido",
                """
                CREATE TRIGGER tr_sancionar_prestamo_vencido
                AFTER UPDATE ON GS_SOLICITUD
                FOR EACH ROW
                BEGIN
                    DECLARE v_identificacion VARCHAR(30);
                    DECLARE v_fecha_limite DATE;
                    DECLARE v_idprestamo INT;
                    DECLARE v_fecha_inicio DATE;
                    DECLARE v_fecha_fin DATE;
                    DECLARE v_sancion_existe INT DEFAULT 0;
                    
                    -- Solo proceder si la solicitud está siendo finalizada
                    IF NEW.ESTADO = 'finalizado' AND OLD.ESTADO != 'finalizado' THEN
                        -- Obtener datos del préstamo asociado
                        SELECT p.IDPRESTAMO, p.FECHA_LIMITE, NEW.IDENTIFICACION
                        INTO v_idprestamo, v_fecha_limite, v_identificacion
                        FROM HS_PRESTAMO p
                        WHERE p.IDSOLICITUD = NEW.IDSOLICITUD
                        LIMIT 1;
                        
                        -- Verificar si la entrega es tardía (fecha actual > fecha límite)
                        IF CURDATE() > v_fecha_limite THEN
                            -- Verificar si ya existe una sanción para este préstamo
                            SELECT COUNT(*) INTO v_sancion_existe
                            FROM GS_SANCION
                            WHERE IDPRESTAMO = v_idprestamo;
                            
                            -- Solo crear sanción si no existe una previa
                            IF v_sancion_existe = 0 THEN
                                -- Calcular fechas de sanción
                                SET v_fecha_inicio = CURDATE();
                                SET v_fecha_fin = DATE_ADD(v_fecha_inicio, INTERVAL 3 DAY);
                                
                                -- Insertar la sanción
                                INSERT INTO GS_SANCION (
                                    IDENTIFICACION,
                                    IDPRESTAMO,
                                    FECHA_INICIO,
                                    FECHA_FIN,
                                    DIAS_SANCION,
                                    MOTIVO,
                                    ESTADO,
                                    FECHA_REGISTRO
                                ) VALUES (
                                    v_identificacion,
                                    v_idprestamo,
                                    v_fecha_inicio,
                                    v_fecha_fin,
                                    3,
                                    'Entrega tardía de préstamo',
                                    'activa',
                                    NOW()
                                );
                                
                                -- Actualizar estado del solicitante a 'no apto'
                                UPDATE GS_SOLICITANTE
                                SET ESTADO = 'no apto'
                                WHERE IDENTIFICACION = v_identificacion;
                            END IF;
                        END IF;
                    END IF;
                END
                """
            ]
            
            for trigger_sql in triggers:
                try:
                    connection.execute(text(trigger_sql))
                    print(f"✅ Trigger ejecutado correctamente")
                except Exception as trigger_error:
                    print(f"⚠️ Error ejecutando trigger: {trigger_error}")

            # Create indexes
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_estado_solicitante ON GS_SOLICITANTE(ESTADO)",
                "CREATE INDEX IF NOT EXISTS idx_rol_solicitante ON GS_SOLICITANTE(ROL)",
                "CREATE INDEX IF NOT EXISTS idx_estado_producto ON GS_PRODUCTO(ESTADO)",
                "CREATE INDEX IF NOT EXISTS idx_estado_solicitud ON GS_SOLICITUD(ESTADO)",
                "CREATE INDEX IF NOT EXISTS idx_fecha_prestamo ON HS_PRESTAMO(FECHA_REGISTRO)",
                "CREATE INDEX IF NOT EXISTS idx_fecha_limite ON HS_PRESTAMO(FECHA_LIMITE)",
                "CREATE INDEX IF NOT EXISTS idx_fecha_prolongacion ON HS_PRESTAMO(FECHA_PROLONGACION)",
                "CREATE INDEX IF NOT EXISTS idx_sancion_identificacion ON GS_SANCION(IDENTIFICACION)",
                "CREATE INDEX IF NOT EXISTS idx_sancion_estado ON GS_SANCION(ESTADO)",
                "CREATE INDEX IF NOT EXISTS idx_sancion_fecha_inicio ON GS_SANCION(FECHA_INICIO)",
                "CREATE INDEX IF NOT EXISTS idx_sancion_fecha_fin ON GS_SANCION(FECHA_FIN)",
                "CREATE INDEX IF NOT EXISTS idx_sancion_prestamo ON GS_SANCION(IDPRESTAMO)"
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
