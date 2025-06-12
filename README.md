# LendIT - Sistema de Gestión de Préstamos

Sistema de gestión de préstamos de equipos y recursos desarrollado con React (Frontend) y FastAPI (Backend).

## Estructura del Proyecto

```
lenditweb/
├── Backend/
│   ├── app/
│   │   ├── api/                    # Rutas y endpoints de la API
│   │   │   ├── auth/              # Autenticación y autorización
│   │   │   ├── prestamos/         # Endpoints de préstamos
│   │   │   ├── productos/         # Endpoints de productos
│   │   │   └── solicitantes/      # Endpoints de solicitantes
│   │   ├── core/                  # Núcleo de la aplicación
│   │   │   ├── config/           # Configuraciones
│   │   │   ├── database/         # Configuración de base de datos
│   │   │   └── security/         # Seguridad y autenticación
│   │   ├── models/               # Modelos SQLAlchemy
│   │   └── schemas/              # Esquemas Pydantic
│   ├── scripts/                  # Scripts de utilidad
│   │   ├── install_mysql.py
│   │   └── setup_mysql.py
│   ├── tests/                    # Pruebas unitarias
│   ├── requirements.txt          # Dependencias del backend
│   └── main.py                   # Punto de entrada del backend
│
├── Frontend/
│   ├── public/                   # Archivos públicos
│   ├── src/
│   │   ├── api/                 # Servicios de API
│   │   ├── components/          # Componentes React
│   │   ├── hooks/              # Custom hooks
│   │   ├── pages/              # Páginas/Rutas
│   │   ├── styles/             # Estilos CSS
│   │   ├── utils/              # Utilidades
│   │   └── App.js              # Componente principal
│   ├── package.json            # Dependencias del frontend
│   └── README.md               # Documentación del frontend
│
└── README.md                    # Documentación principal
```

## Características

- Gestión de préstamos de equipos
- Control de inventario
- Gestión de solicitantes
- Sistema de autenticación
- Reportes y estadísticas

## Tecnologías

### Backend
- FastAPI
- SQLAlchemy
- MySQL
- JWT Authentication

### Frontend
- React
- Bootstrap
- Axios
- React Router

## Instalación

1. Clonar el repositorio
2. Configurar el backend:
   ```bash
   cd Backend
   pip install -r requirements.txt
   python setup_mysql.py
   ```

3. Configurar el frontend:
   ```bash
   cd Frontend
   npm install
   ```

## Ejecución

1. Iniciar el backend:
   ```bash
   cd Backend
python -m uvicorn main:app --reload   ```

2. Iniciar el frontend:
   ```bash
   cd Frontend
   npm start
   ```

## Acceso

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Documentación API: http://localhost:8000/docs

## Credenciales por defecto

- Usuario: 1234567890
- Contraseña: admin

## Contribución

1. Fork el repositorio
2. Crea una rama para tu funcionalidad (git checkout -b feature/AmazingFeature)
3. Haz commit de tus cambios (git commit -m 'agregar mejoras')
4. Push a la rama
5. Abra un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
