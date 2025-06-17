# Sistema de Sanciones Automáticas

## Descripción General

Se ha implementado un sistema automático de sanciones que se activa cuando un solicitante no entrega un producto antes de la fecha límite establecida. El sistema funciona mediante triggers de base de datos y APIs para gestionar las sanciones.

## Componentes Implementados

### 1. Tabla de Sanciones (GS_SANCION)

```sql
CREATE TABLE GS_SANCION (
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
```

### 2. Trigger Automático (tr_sancionar_prestamo_vencido)

El trigger se ejecuta automáticamente cuando:
- Una solicitud cambia su estado a 'finalizado'
- La fecha actual es posterior a la fecha límite del préstamo
- No existe una sanción previa para ese préstamo

**Acciones del trigger:**
1. Verifica si la entrega es tardía
2. Crea una sanción de 3 días
3. Cambia el estado del solicitante a 'no apto'

### 3. API de Sanciones

**Endpoints disponibles:**

#### GET /api/sanciones/
- Obtiene todas las sanciones con información del solicitante y préstamo

#### GET /api/sanciones/activas
- Obtiene solo las sanciones activas

#### GET /api/sanciones/solicitante/{identificacion}
- Obtiene sanciones de un solicitante específico

#### PUT /api/sanciones/{sancion_id}/cumplir
- Marca una sanción como cumplida
- Restaura el estado del solicitante a 'apto' si no tiene otras sanciones activas

#### PUT /api/sanciones/{sancion_id}/cancelar
- Cancela una sanción
- Restaura el estado del solicitante a 'apto' si no tiene otras sanciones activas

#### GET /api/sanciones/vencidas
- Verifica y actualiza automáticamente sanciones que han vencido

## Flujo de Funcionamiento

### 1. Creación Automática de Sanción

```
Préstamo vencido → Finalizar solicitud → Trigger se activa → 
Crear sanción → Cambiar estado solicitante a 'no apto'
```

### 2. Gestión de Sanciones

```
Sanción activa → Cumplir/Cancelar → Verificar otras sanciones → 
Si no hay más sanciones activas → Restaurar estado a 'apto'
```

### 3. Vencimiento Automático

```
Sanción activa + Fecha fin < Hoy → Marcar como cumplida → 
Restaurar estado si no hay más sanciones
```

## Características del Sistema

### Duración de Sanciones
- **Por defecto:** 3 días
- **Configurable:** Se puede modificar en la tabla

### Estados de Sanción
- **activa:** Sanción en vigor
- **cumplida:** Sanción completada (por tiempo o manualmente)
- **cancelada:** Sanción anulada por administrador

### Estados de Solicitante
- **apto:** Puede realizar préstamos
- **no apto:** No puede realizar préstamos (tiene sanciones activas)

### Prevención de Duplicados
- El trigger verifica que no exista una sanción previa para el mismo préstamo
- Evita sanciones múltiples por el mismo incidente

## Índices para Rendimiento

```sql
CREATE INDEX idx_sancion_identificacion ON GS_SANCION(IDENTIFICACION);
CREATE INDEX idx_sancion_estado ON GS_SANCION(ESTADO);
CREATE INDEX idx_sancion_fecha_inicio ON GS_SANCION(FECHA_INICIO);
CREATE INDEX idx_sancion_fecha_fin ON GS_SANCION(FECHA_FIN);
CREATE INDEX idx_sancion_prestamo ON GS_SANCION(IDPRESTAMO);
```

## Casos de Uso

### 1. Préstamo Entregado a Tiempo
- No se genera sanción
- Solicitante mantiene estado 'apto'

### 2. Préstamo Entregado Tarde
- Se genera sanción automáticamente
- Solicitante pasa a estado 'no apto'
- Duración: 3 días desde la fecha de entrega

### 3. Múltiples Sanciones
- Un solicitante puede tener múltiples sanciones
- Permanece 'no apto' mientras tenga al menos una sanción activa
- Solo vuelve a 'apto' cuando todas las sanciones están cumplidas/canceladas

### 4. Gestión Administrativa
- Los administradores pueden cancelar sanciones
- Pueden marcar sanciones como cumplidas manualmente
- Sistema verifica automáticamente sanciones vencidas

## Integración con el Sistema Existente

### Validaciones de Préstamo
- El sistema debe verificar el estado del solicitante antes de aprobar nuevos préstamos
- Solicitantes con estado 'no apto' no pueden recibir nuevos préstamos

### Notificaciones (Futuro)
- Se puede implementar un sistema de notificaciones para:
  - Alertar sobre sanciones próximas a vencer
  - Notificar cuando un solicitante es sancionado
  - Informar cuando una sanción es cumplida

## Mantenimiento

### Verificación Periódica
- Ejecutar `/api/sanciones/vencidas` periódicamente para actualizar sanciones vencidas
- Se recomienda ejecutar diariamente mediante un cron job

### Monitoreo
- Revisar logs de triggers para detectar errores
- Monitorear la tabla de sanciones para identificar patrones

## Consideraciones de Seguridad

- Solo usuarios autorizados pueden cancelar sanciones
- El trigger es automático y no puede ser manipulado por usuarios
- Las fechas se calculan automáticamente para evitar manipulación
