# LendIT Backend

API REST para el sistema de gestión de préstamos LendIT desarrollada con FastAPI.

## Estructura del Proyecto

```
Backend/
├── app/
│   ├── api/                    # Endpoints de la API
│   │   ├── auth/              # Autenticación
│   │   │   └── login.py       # Login de usuarios
│   │   ├── prestamos/         # Gestión de préstamos
│   │   │   ├── prestamo.py    # CRUD de préstamos
│   │   │   └── prestamo_validacion.py
│   │   ├── productos/         # Gestión de productos
│   │   │   ├── producto.py    # CRUD de productos
│   │   │   ├── producto_router.py
│   │   │   ├── tipo_producto.py
│   │   │   └── tipo_producto_router.py
│   │   └── solicitantes/      # Gestión de solicitantes
│   │       └── solicitante.py # CRUD de solicitantes
│   ├── core/                  # Núcleo de la aplicación
│   │   ├── config/           # Configuraciones
│   │   │   └── settings.py   # Configuración principal
│   │   ├── database/         # Modelos de base de datos
│   │   │   ├── db.py         # Configuración de SQLAlchemy
│   │   │   ├── init_mysql.py # Inicialización de MySQL
│   │   │   ├── usuario.py    # Modelo de usuario
│   │   │   ├── solicitante.py # Modelo de solicitante
│   │   │   ├── producto.py   # Modelo de producto
│   │   │   ├── prestamo.py   # Modelo de préstamo
│   │   │   └── ...           # Otros modelos
│   │   └── security/         # Seguridad (vacío por ahora)
│   ├── models/               # Modelos SQLAlchemy (legacy)
│   └── schemas/              # Esquemas Pydantic
│       ├── usuario_modelo.py
│       ├── solicitante_modelo.py
│       ├── producto_modelo.py
│       └── prestamo_modelo.py
├── scripts/                  # Scripts de utilidad
│   ├── create_admin.py       # Crear usuario administrador
│   ├── install_mysql.py      # Instalación de MySQL
│   ├── migrate_data.py       # Migración de datos
│   └── setup_mysql.py        # Configuración de MySQL
├── tests/                    # Pruebas unitarias (vacío)
├── main.py                   # Punto de entrada de la aplicación
└── requirements.txt          # Dependencias de Python
```

## Tecnologías Utilizadas

- **FastAPI** - Framework web moderno y rápido para Python
- **SQLAlchemy** - ORM para Python
- **MySQL** - Base de datos relacional
- **Pydantic** - Validación de datos usando type hints
- **JWT** - Autenticación basada en tokens
- **Uvicorn** - Servidor ASGI

## Instalación

1. Crear un entorno virtual:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Configurar MySQL:
   ```bash
   python scripts/setup_mysql.py
   ```

4. Crear usuario administrador:
   ```bash
   python scripts/create_admin.py
   ```

## Ejecución

```bash
python main.py
```

La API estará disponible en:
- **Aplicación**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **Redoc**: http://localhost:8000/redoc

## Configuración

La configuración se encuentra en `app/core/config/settings.py`:

- **DATABASE_URL**: URL de conexión a MySQL
- **JWT_SECRET**: Clave secreta para JWT
- **CORS_ORIGINS**: Orígenes permitidos para CORS

## Endpoints Principales

### Autenticación
- `POST /usuario/login` - Iniciar sesión

### Solicitantes
- `GET /solicitantes/obtener` - Obtener todos los solicitantes
- `POST /solicitantes/registrar` - Registrar nuevo solicitante
- `PUT /solicitantes/actualizar/{id}` - Actualizar solicitante
- `DELETE /solicitantes/eliminar/{id}` - Eliminar solicitante
- `POST /solicitantes/importar-excel` - Importar desde Excel

### Productos
- `GET /productos/` - Obtener todos los productos
- `POST /productos/registrar` - Registrar nuevo producto
- `PUT /productos/actualizar/{id}` - Actualizar producto
- `DELETE /productos/eliminar/{id}` - Eliminar producto
- `GET /productos/contadores` - Obtener contadores

### Tipos de Producto
- `GET /tipos-producto/` - Obtener tipos de producto
- `POST /tipos-producto/` - Crear tipo de producto

### Préstamos
- `GET /prestamo/` - Obtener préstamos
- `POST /prestamo/registrar` - Registrar préstamo
- `PUT /prestamo/devolver/{id}` - Devolver préstamo

## Base de Datos

La aplicación utiliza MySQL con las siguientes tablas principales:

- **GS_USUARIO** - Usuarios del sistema
- **HS_SOLICITANTE** - Solicitantes de préstamos
- **HS_PRODUCTO** - Productos disponibles
- **HS_TIPO_PRODUCTO** - Tipos de productos
- **HS_PRESTAMO** - Préstamos registrados
- **HS_PROGRAMAS** - Programas de formación
- **HS_FICHA** - Fichas de formación

## Desarrollo

Para contribuir al proyecto:

1. Fork el repositorio
2. Crear una rama para la nueva funcionalidad
3. Realizar los cambios
4. Ejecutar las pruebas
5. Crear un Pull Request

## Scripts Útiles

- `python scripts/setup_mysql.py` - Configurar base de datos
- `python scripts/create_admin.py` - Crear usuario admin
- `python scripts/migrate_data.py` - Migrar datos existentes
