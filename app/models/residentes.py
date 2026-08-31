from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class Residente(Base):
    __tablename__ = "residentes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    pin = Column(String, nullable=True)
    rol = Column(String, default="residente")  # administrador / residente
    activo = Column(Boolean, default=True)
    creado_en = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    condominio_id = Column(Integer, ForeignKey("condominios.id"), nullable=False)

    condominio = relationship("Condominio", back_populates="residentes")
    vehiculos = relationship("Vehiculo", back_populates="residente")
    tokens_visitante = relationship("Visitante", back_populates="creado_por")