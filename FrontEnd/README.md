# LenditWeb - Sistema de Gestión de Préstamos

## Descripción
LenditWeb es una aplicación web diseñada para gestionar préstamos de equipos y recursos. El sistema permite administrar solicitantes, realizar seguimiento de préstamos y gestionar el inventario de manera eficiente.

## Requisitos del Sistema
- Node.js (versión 14 o superior)
- Python (versión 3.8 o superior)
- Base de datos SQLite

## Instalación

### Frontend (React)
1. Navegar al directorio del frontend:
```bash
cd FrontEnd
```

2. Instalar dependencias:
```bash
npm install
```

3. Iniciar la aplicación en modo desarrollo:
```bash
npm start
```

### Backend (Python/FastAPI)
1. Navegar al directorio del backend:
```bash
cd Backend
```

2. Instalar dependencias de Python:
```bash
pip install -r requirements.txt
```

3. Iniciar el servidor:
```bash
python main.py
```

## Uso del Sistema

### 1. Gestión de Solicitantes
- **Panel de Solicitantes**: Acceda a la gestión completa de solicitantes desde el menú principal.
- **Agregar Solicitante**: Use el botón "+" para registrar nuevos solicitantes.
- **Editar/Eliminar**: Seleccione un solicitante de la tabla y use los botones correspondientes.
- **Importar Datos**: Utilice la función de importación para cargar múltiples solicitantes desde un archivo Excel.
- **Filtrar**: Use los campos de búsqueda para filtrar por identificación o número de ficha.

### 2. Gestión de Préstamos
- Registro de préstamos nuevos
- Seguimiento del estado de préstamos
- Devolución de equipos
- Historial de préstamos

### 3. Inventario
- Control de equipos disponibles
- Registro de nuevos equipos
- Actualización de estado de equipos
- Reportes de inventario

## Funcionalidades Principales

### Panel de Solicitantes
- Visualización de lista completa de solicitantes
- Filtros por identificación y número de ficha
- Gestión CRUD (Crear, Leer, Actualizar, Eliminar)
- Importación masiva de datos

### Sistema de Préstamos
- Registro de préstamos
- Control de devoluciones
- Seguimiento en tiempo real
- Notificaciones de estado

### Gestión de Inventario
- Control de stock
- Categorización de equipos
- Estado de equipos
- Reportes y estadísticas

## Soporte

Para reportar problemas o solicitar ayuda, por favor crear un issue en el repositorio de GitHub:
https://github.com/Santiago5626/lenditweb

## Contribuir
Las contribuciones son bienvenidas. Por favor, asegúrese de actualizar las pruebas según corresponda.
