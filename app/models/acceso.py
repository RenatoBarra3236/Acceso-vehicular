from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class Acceso(Base):
    __tablename__ = "accesos"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, nullable=False)           # entrada / salida
    metodo_acceso = Column(String, nullable=False)  # BLE / PIN / QR / manual
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    vehiculo_id = Column(Integer, ForeignKey("vehiculos.id"), nullable=True)
    visitante_id = Column(Integer, ForeignKey("visitantes.id"), nullable=True)

    vehiculo = relationship("Vehiculo", back_populates="accesos")
    visitante = relationship("Visitante", back_populates="accesos")
