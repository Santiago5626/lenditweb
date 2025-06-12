from sqlalchemy import Column, Integer, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base

class ConteoDiario(Base):
    __tablename__ = "GS_CONTEO_DIARIO"
    
    idConteo = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(Date, nullable=False)
    jornada = Column(Enum('mañana', 'tarde', name='jornada_enum'), nullable=False)
    idProducto = Column(Integer, ForeignKey("GS_PRODUCTO.IDPRODUCTO"), nullable=False)
    cantidadDisponible = Column(Integer, nullable=False)

    # Relationship
    producto = relationship("Producto")

    def __repr__(self):
        return f"<ConteoDiario(id={self.idConteo}, fecha='{self.fecha}', jornada='{self.jornada}', producto={self.idProducto})>"
