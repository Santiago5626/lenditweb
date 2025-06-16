# Actualización del Flujo de Solicitudes y Préstamos

## Resumen de Cambios Implementados

### 1. Nuevas Tablas en la Base de Datos

#### Tabla `solicitud`
- `IDSOLICITUD` (PK, AUTO_INCREMENT)
- `IDENTIFICACION` (VARCHAR(20), FK a solicitante)
- `FECHA_REGISTRO` (DATE)
- `ESTADO` (ENUM: 'pendiente', 'aprobado', 'rechazado', 'finalizado')

#### Tabla `producto_solicitud`
- `IDPRODUCTOSOLICITUD` (PK, AUTO_INCREMENT)
- `PRODUCTO_ID` (INT, FK a producto)
- `SOLICITUD_ID` (INT, FK a solicitud)

#### Tabla Actualizada `prestamo`
- `IDPRESTAMO` (PK, AUTO_INCREMENT)
- `IDSOLICITUD` (INT, FK a solicitud) - **NUEVO CAMPO**
- `FECHA_REGISTRO` (DATE)
- `FECHA_LIMITE` (DATE)
- `FECHA_PROLONGACION` (DATE, nullable)

### 2. Nuevos Modelos SQLAlchemy

#### `app/core/database/solicitud.py`
```python
class Solicitud(Base):
    __tablename__ = "solicitud"
    
    IDSOLICITUD = Column(Integer, primary_key=True, index=True, autoincrement=True)
    IDENTIFICACION = Column(String(20), ForeignKey("solicitante.identificacion"), nullable=False)
    FECHA_REGISTRO = Column(Date, nullable=False)
    ESTADO = Column(Enum('pendiente', 'aprobado', 'rechazado', 'finalizado'), default='pendiente')
```

#### `app/core/database/producto_solicitud.py`
```python
class ProductoSolicitud(Base):
    __tablename__ = "producto_solicitud"
    
    IDPRODUCTOSOLICITUD = Column(Integer, primary_key=True, index=True, autoincrement=True)
    PRODUCTO_ID = Column(Integer, ForeignKey("producto.IDPRODUCTO"), nullable=False)
    SOLICITUD_ID = Column(Integer, ForeignKey("solicitud.IDSOLICITUD"), nullable=False)
```

### 3. Nuevos Endpoints de API

#### Router de Solicitudes (`app/api/solicitudes/solicitud.py`)

**GET /solicitudes/obtener**
- Obtiene todas las solicitudes

**POST /solicitudes/crear**
- Crea una nueva solicitud
- Body: `{IDENTIFICACION, FECHA_REGISTRO, ESTADO}`

**POST /solicitudes/agregar-producto**
- Agrega un producto a una solicitud
- Body: `{PRODUCTO_ID, SOLICITUD_ID}`

**PUT /solicitudes/actualizar-estado**
- Actualiza el estado de una solicitud
- Body: `{solicitud_id, nuevo_estado}`

**GET /solicitudes/buscar/{solicitud_id}**
- Busca una solicitud específica

### 4. Actualizaciones en el Frontend

#### Nuevas Funciones API (`FrontEnd/src/api/peticiones.js`)

```javascript
// Funciones para solicitudes
export async function fetchSolicitudes()
export async function crearSolicitud(solicitudData)
export async function agregarProductoASolicitud(productoSolicitudData)
export async function actualizarEstadoSolicitud(solicitudData)

// Funciones actualizadas para préstamos
export async function crearPrestamo(prestamoData) // Ahora usa IDSOLICITUD
export async function fetchPrestamos() // Incluye datos de solicitud
```

#### Componente Actualizado (`FrontEnd/src/components/TablaPrestamos.jsx`)
- Muestra información de solicitudes y productos asociados
- Maneja múltiples productos por préstamo
- Estados actualizados: pendiente, aprobado, rechazado, finalizado

#### Estilos Actualizados (`FrontEnd/src/styles/components/TablaPrestamos.css`)
- Nuevos estilos para estados de solicitud
- Estilos para lista de productos
- Responsive design mejorado

### 5. Nuevo Flujo de Trabajo

#### Proceso de Creación de Préstamos:

1. **Crear Solicitud**
   ```javascript
   const solicitudData = {
     IDENTIFICACION: solicitante.identificacion,
     FECHA_REGISTRO: new Date().toISOString().split('T')[0],
     ESTADO: 'pendiente'
   };
   const solicitud = await crearSolicitud(solicitudData);
   ```

2. **Agregar Productos a la Solicitud**
   ```javascript
   await Promise.all(productos.map(producto => 
     agregarProductoASolicitud({
       PRODUCTO_ID: producto.IDPRODUCTO,
       SOLICITUD_ID: solicitud.IDSOLICITUD
     })
   ));
   ```

3. **Crear Préstamo**
   ```javascript
   const prestamoData = {
     IDSOLICITUD: solicitud.IDSOLICITUD,
     FECHA_REGISTRO: new Date().toISOString().split('T')[0],
     FECHA_LIMITE: fechaLimite
   };
   await crearPrestamo(prestamoData);
   ```

### 6. Actualizaciones en el Backend

#### Endpoint de Préstamos Actualizado
- `/prestamo/obtener` ahora incluye datos de solicitud y productos
- `/prestamo/crear` usa `IDSOLICITUD` en lugar de campos individuales
- `/prestamo/actualizarEstado` actualiza el estado de la solicitud asociada

#### Relaciones de Base de Datos
- Un préstamo está vinculado a una solicitud
- Una solicitud puede tener múltiples productos
- Un solicitante puede tener múltiples solicitudes

### 7. Estados del Sistema

#### Estados de Solicitud:
- **pendiente**: Solicitud creada, esperando aprobación
- **aprobado**: Solicitud aprobada, préstamo activo
- **rechazado**: Solicitud rechazada
- **finalizado**: Préstamo completado/devuelto

### 8. Beneficios del Nuevo Sistema

1. **Trazabilidad Mejorada**: Cada préstamo está vinculado a una solicitud específica
2. **Múltiples Productos**: Una solicitud puede incluir varios productos
3. **Gestión de Estados**: Control granular del estado de solicitudes
4. **Historial Completo**: Registro completo del proceso de solicitud a devolución
5. **Escalabilidad**: Estructura preparada para futuras funcionalidades

### 9. Archivos Modificados

#### Backend:
- `Backend/main.py` - Agregado router de solicitudes
- `Backend/app/api/solicitudes/solicitud.py` - Nuevo router
- `Backend/app/api/prestamos/prestamo.py` - Endpoints actualizados
- `Backend/app/core/database/solicitud.py` - Nuevo modelo
- `Backend/app/core/database/producto_solicitud.py` - Nuevo modelo
- `Backend/app/core/database/prestamo.py` - Modelo actualizado

#### Frontend:
- `FrontEnd/src/api/peticiones.js` - Nuevas funciones API
- `FrontEnd/src/pages/Circulacion.jsx` - Flujo actualizado
- `FrontEnd/src/components/TablaPrestamos.jsx` - Componente actualizado
- `FrontEnd/src/styles/components/TablaPrestamos.css` - Estilos actualizados

### 10. Próximos Pasos Recomendados

1. **Migración de Datos**: Ejecutar script de migración para datos existentes
2. **Pruebas**: Verificar funcionamiento completo del nuevo flujo
3. **Documentación**: Actualizar documentación de usuario
4. **Capacitación**: Entrenar usuarios en el nuevo flujo de trabajo

## Notas Importantes

- El sistema mantiene compatibilidad con la estructura existente
- Los datos existentes pueden migrarse al nuevo formato
- El nuevo flujo es más robusto y escalable
- Se recomienda realizar pruebas exhaustivas antes del despliegue en producción
