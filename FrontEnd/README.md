# LendIT Frontend

Frontend de la aplicación LendIT desarrollado con React.

## Estructura del Proyecto

```
src/
├── api/                    # Servicios de API
│   ├── auth.js            # Autenticación
│   └── peticiones.js      # Peticiones HTTP
├── components/            # Componentes React
│   ├── EditarModal.jsx
│   ├── EditarProductoModal.jsx
│   ├── ImportarSolicitantesModal.jsx
│   ├── PaginationControls.jsx
│   ├── PanelSolicitante.jsx
│   ├── ProtectedRoute.jsx
│   ├── RegistrarModal.jsx
│   ├── RegistrarPrestamoModal.jsx
│   ├── RegistrarProductoModal.jsx
│   ├── ResumenTarjetas.jsx
│   ├── Sidebar.jsx
│   ├── TablaInventario.jsx
│   ├── TablaSolicitantes.jsx
│   ├── TablaSolicitantesTable.jsx
│   └── TablaSolicitantesTableSimple.jsx
├── hooks/                 # Custom hooks (vacío por ahora)
├── images/               # Imágenes y recursos
│   ├── logo.png
│   └── perfil.png
├── pages/                # Páginas/Rutas principales
│   ├── Circulacion.jsx
│   ├── inicio.jsx
│   ├── Inventario.jsx
│   ├── login.jsx
│   └── Reportes.jsx
├── styles/               # Estilos CSS organizados
│   ├── components/       # Estilos de componentes
│   │   ├── RegistrarModal.css
│   │   ├── ResumenTarjetas.css
│   │   ├── Sidebar.css
│   │   ├── TablaInventario.css
│   │   └── TablaSolicitantes.css
│   ├── pages/           # Estilos de páginas
│   │   ├── inicio.css
│   │   └── Login.css
│   ├── layout/          # Estilos de layout
│   │   └── layout.css
│   └── App.css          # Estilos globales
├── utils/               # Utilidades (vacío por ahora)
├── App.js               # Componente principal
└── index.js             # Punto de entrada
```

## Tecnologías Utilizadas

- **React** - Biblioteca de JavaScript para interfaces de usuario
- **React Router** - Enrutamiento para aplicaciones React
- **Bootstrap** - Framework CSS para diseño responsivo
- **Axios** - Cliente HTTP para realizar peticiones a la API

## Instalación

1. Instalar dependencias:
   ```bash
   npm install
   ```

2. Iniciar el servidor de desarrollo:
   ```bash
   npm start
   ```

3. Abrir [http://localhost:3000](http://localhost:3000) en el navegador

## Scripts Disponibles

- `npm start` - Inicia el servidor de desarrollo
- `npm run build` - Construye la aplicación para producción
- `npm test` - Ejecuta las pruebas
- `npm run eject` - Expone la configuración de webpack

## Características

- **Gestión de Solicitantes**: Registro, edición y visualización de solicitantes
- **Control de Inventario**: Gestión de productos y tipos de productos
- **Sistema de Préstamos**: Registro y seguimiento de préstamos
- **Importación de Datos**: Importación masiva desde archivos Excel
- **Autenticación**: Sistema de login con protección de rutas
- **Interfaz Responsiva**: Diseño adaptable a diferentes dispositivos

## Configuración de la API

La aplicación se conecta al backend en `http://localhost:8000`. Para cambiar esta configuración, modifica los archivos en `src/api/`.

## Estructura de Estilos

Los estilos están organizados por categorías:
- **components/**: Estilos específicos de componentes
- **pages/**: Estilos específicos de páginas
- **layout/**: Estilos de diseño general
- **App.css**: Estilos globales de la aplicación
