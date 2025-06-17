# Sistema de Refresh Token - LendItWeb

## Descripción

Se ha implementado un sistema de refresh token para mantener la sesión activa cuando hay actividad reciente del usuario, evitando que se cierre la sesión automáticamente durante el uso activo de la aplicación.

## Características Implementadas

### Frontend (FrontEnd/src/api/auth.js)

#### 1. **Detección de Actividad del Usuario**
- Monitorea eventos: `mousedown`, `keydown`, `scroll`, `touchstart`
- Actualiza automáticamente el timestamp de última actividad
- Configura listeners al inicializar la aplicación

#### 2. **Temporizador de Inactividad**
- **Tiempo límite**: 30 minutos de inactividad
- Se reinicia automáticamente con cada actividad del usuario
- Cierra sesión automáticamente tras el período de inactividad

#### 3. **Refresh Token Automático**
- Se ejecuta cuando hay actividad reciente (últimos 5 minutos)
- Renueva el token JWT automáticamente
- Mantiene la sesión activa sin interrupciones

#### 4. **Funciones Principales**

```javascript
// Inicializar sistema al cargar la aplicación
initializeAuth()

// Refrescar token manualmente
refreshToken()

// Reiniciar temporizador de inactividad
resetInactivityTimer()

// Configurar listeners de actividad
setupActivityListeners()
```

### Backend (Backend/app/api/auth/login.py)

#### 1. **Endpoint de Refresh Token**
- **Ruta**: `POST /usuario/refresh-token`
- **Autenticación**: Bearer Token requerido
- Acepta tokens expirados para renovación
- Verifica existencia del usuario en base de datos

#### 2. **Funcionalidades del Endpoint**
- Decodifica token actual (incluso si está expirado)
- Valida datos del usuario (user_id, nombre)
- Verifica que el usuario existe en la base de datos
- Genera nuevo token JWT con nueva expiración
- Retorna el nuevo token al frontend

#### 3. **Seguridad**
- Validación de token existente
- Verificación de usuario en base de datos
- Manejo de errores y tokens inválidos
- Logs de errores para debugging

## Configuración

### Parámetros Configurables

```javascript
// Tiempo de inactividad antes de cerrar sesión (minutos)
const INACTIVITY_TIMEOUT = 30;

// Tiempo para refresh automático (minutos)
const AUTO_REFRESH_THRESHOLD = 5;
```

### Configuración Backend

```python
# Tiempo de expiración del token (segundos)
JWT_EXP_DELTA_SECONDS = 3600  # 1 hora

# Clave secreta JWT
JWT_SECRET = "your_jwt_secret_key"
```

## Flujo de Funcionamiento

### 1. **Inicio de Sesión**
1. Usuario inicia sesión exitosamente
2. Se configura el sistema de refresh token
3. Se inician los listeners de actividad
4. Se establece el temporizador de inactividad

### 2. **Durante el Uso**
1. Usuario interactúa con la aplicación
2. Se detecta actividad y se reinicia el temporizador
3. Si hay actividad reciente (< 5 min), se refresca el token automáticamente
4. El token se renueva sin interrumpir la experiencia del usuario

### 3. **Inactividad**
1. Usuario no interactúa por 30 minutos
2. Se ejecuta logout automático
3. Se limpia el localStorage
4. Se redirige a la página de login

### 4. **Refresh de Token**
1. Frontend detecta actividad reciente
2. Envía request al endpoint `/refresh-token`
3. Backend valida el token actual
4. Se genera nuevo token con nueva expiración
5. Frontend actualiza el token en localStorage

## Mejoras de Redirección

### 1. **ProtectedRoute Mejorado**
- Verificación asíncrona del token en el servidor
- Loading spinner durante la verificación
- Redirección automática cuando el token expira
- Evita páginas en blanco durante la validación

### 2. **Interceptor de Axios**
- Manejo global de errores de autenticación
- Redirección automática en errores 401/403
- Headers de autorización automáticos
- Timeout configurable para peticiones

### 3. **Manejo de Errores Mejorado**
- Función centralizada para manejo de errores
- Diferenciación entre tipos de error
- Mensajes de error más descriptivos
- Prevención de redirecciones innecesarias

## Beneficios

### Para el Usuario
- **Sesión continua**: No se interrumpe durante el uso activo
- **Seguridad**: Cierre automático tras inactividad prolongada
- **Experiencia fluida**: Renovación transparente del token
- **Sin páginas en blanco**: Redirección inmediata cuando expira el token

### Para el Sistema
- **Seguridad mejorada**: Tokens con tiempo de vida limitado
- **Gestión automática**: No requiere intervención manual
- **Monitoreo de actividad**: Tracking de uso real de la aplicación
- **Manejo robusto de errores**: Interceptores globales para autenticación

## Integración

### Inicialización en App.js
```javascript
import { initializeAuth } from './api/auth';

function App() {
  useEffect(() => {
    initializeAuth();
  }, []);
  // ...
}
```

### Uso en Componentes
El sistema funciona automáticamente una vez inicializado. No requiere código adicional en los componentes.

## Consideraciones Técnicas

### Rendimiento
- Listeners optimizados para no afectar performance
- Throttling automático de requests de refresh
- Limpieza de timers al cerrar sesión

### Compatibilidad
- Funciona en todos los navegadores modernos
- Soporte para dispositivos móviles (touchstart)
- Manejo de errores robusto

### Mantenimiento
- Logs detallados para debugging
- Configuración centralizada
- Código modular y reutilizable

## Próximas Mejoras

1. **Configuración dinámica**: Permitir ajustar tiempos desde admin
2. **Notificaciones**: Avisar al usuario antes del cierre por inactividad
3. **Métricas**: Tracking de patrones de uso y sesiones
4. **Refresh token persistente**: Implementar refresh tokens de larga duración
