from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.core.database.prestamo import Prestamo
from app.core.database.solicitante import Solicitante
from app.core.database.producto import Producto

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
    prestamos_activos = db.query(Prestamo).filter(
        Prestamo.IDENTIFICACION_SOLICITANTE == identificacion_solicitante,
        Prestamo.FECHA_DEVOLUCION == None
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
