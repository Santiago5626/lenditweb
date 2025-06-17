from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.core.database.prestamo import Prestamo
from app.core.database.solicitante import Solicitante
from app.core.database.producto import Producto
from app.core.database.tipo_producto import TipoProducto
from app.core.database.solicitud import Solicitud
from app.core.database.producto_solicitud import ProductoSolicitud

class PrestamoValidacionError(Exception):
    pass

def validar_prestamo(db: Session, identificacion_solicitante: str, fecha_limite: datetime):
    """
    Valida si un solicitante puede realizar un préstamo
    """
    # Verificar si el solicitante existe
    solicitante = db.query(Solicitante).filter(Solicitante.IDENTIFICACION == identificacion_solicitante).first()
    if not solicitante:
        raise PrestamoValidacionError("El solicitante no existe")

    # Verificar si el solicitante está apto
    if solicitante.ESTADO != 'apto':
        raise PrestamoValidacionError("El solicitante no está apto para realizar préstamos")

    # Verificar si la fecha límite es válida (no puede ser anterior a la fecha actual)
    if fecha_limite < datetime.now().date():
        raise PrestamoValidacionError("La fecha límite no puede ser anterior a la fecha actual")

    # Verificar si la fecha límite no excede el máximo permitido (por ejemplo, 30 días)
    max_dias = 30
    fecha_maxima = datetime.now().date() + timedelta(days=max_dias)
    if fecha_limite > fecha_maxima:
        raise PrestamoValidacionError(f"La fecha límite no puede exceder {max_dias} días")

    # Verificar si el solicitante tiene préstamos activos
    from app.core.database.solicitud import Solicitud
    
    prestamos_activos = db.query(Prestamo).join(Solicitud).filter(
        Solicitud.IDENTIFICACION == identificacion_solicitante,
        Solicitud.ESTADO.in_(['pendiente', 'aprobado'])
    ).count()

    # Definir límites por rol
    limites_prestamos = {
        'aprendiz': 1,
        'instructor': 2,
        'funcionario': 2,
        'contratista': 2
    }

    limite = limites_prestamos.get(solicitante.ROL, 1)  # Por defecto 1 si el rol no está definido
    if prestamos_activos >= limite:
        raise PrestamoValidacionError(f"El solicitante ya tiene el máximo de préstamos permitidos ({limite})")

    return True

def validar_productos_solicitud(db: Session, identificacion_solicitante: str, productos_ids: list):
    """
    Valida si un solicitante puede solicitar los productos específicos
    """
    # Verificar si el solicitante existe
    solicitante = db.query(Solicitante).filter(Solicitante.IDENTIFICACION == identificacion_solicitante).first()
    if not solicitante:
        raise PrestamoValidacionError("El solicitante no existe")

    # Verificar si el solicitante está apto
    if solicitante.ESTADO != 'apto':
        raise PrestamoValidacionError("El solicitante no está apto para realizar préstamos")

    # Validación específica para aprendices y equipos de cómputo
    if solicitante.ROL.lower() == 'aprendiz':
        # Obtener el tipo de producto "equipo de cómputo"
        tipo_equipo_computo = db.query(TipoProducto).filter(
            TipoProducto.NOMBRE_TIPO_PRODUCTO.ilike('%equipo%computo%')
        ).first()
        
        if not tipo_equipo_computo:
            tipo_equipo_computo = db.query(TipoProducto).filter(
                TipoProducto.NOMBRE_TIPO_PRODUCTO.ilike('%equipo de computo%')
            ).first()
        
        if tipo_equipo_computo:
            # Verificar si alguno de los productos solicitados es equipo de cómputo
            productos_equipo_computo = []
            for producto_id in productos_ids:
                producto = db.query(Producto).filter(Producto.IDPRODUCTO == producto_id).first()
                if producto and producto.IDTIPOPRODUCTO == tipo_equipo_computo.IDTIPOPRODUCTO:
                    productos_equipo_computo.append(producto)
            
            if productos_equipo_computo:
                # Verificar si el aprendiz ya tiene un equipo de cómputo prestado
                # Buscar préstamos activos del solicitante
                prestamos_activos = db.query(Prestamo).join(Solicitud).filter(
                    Solicitud.IDENTIFICACION == identificacion_solicitante,
                    Solicitud.ESTADO.in_(['pendiente', 'aprobado'])
                ).all()
                
                for prestamo in prestamos_activos:
                    # Verificar productos de cada préstamo activo
                    productos_prestamo = db.query(ProductoSolicitud).filter(
                        ProductoSolicitud.SOLICITUD_ID == prestamo.IDSOLICITUD
                    ).all()
                    
                    for ps in productos_prestamo:
                        producto_prestado = db.query(Producto).filter(
                            Producto.IDPRODUCTO == ps.PRODUCTO_ID
                        ).first()
                        
                        if (producto_prestado and 
                            producto_prestado.IDTIPOPRODUCTO == tipo_equipo_computo.IDTIPOPRODUCTO):
                            raise PrestamoValidacionError(
                                "Los aprendices no pueden solicitar más de un equipo de cómputo. "
                                "Ya tienes un equipo de cómputo prestado."
                            )
                
                # Verificar si está solicitando más de un equipo de cómputo en esta solicitud
                if len(productos_equipo_computo) > 1:
                    raise PrestamoValidacionError(
                        "Los aprendices no pueden solicitar más de un equipo de cómputo por solicitud."
                    )

    return True
