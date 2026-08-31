from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class Visitante(Base):
    __tablename__ = "visitantes"

    id = Column(Integer, primary_key=True, index=True)
    token_acceso = Column(String, unique=True, nullable=False, index=True)
    nombre = Column(String, nullable=True)
    creado_por_id = Column(Integer, ForeignKey("residentes.id"), nullable=False)
    valido_desde = Column(DateTime, nullable=False)
    valido_hasta = Column(DateTime, nullable=False)
    usos_maximos = Column(Integer, default=1)
    usos_actuales = Column(Integer, default=0)
    revocado = Column(Boolean, default=False)
    creado_en = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    creado_por = relationship("Residente", back_populates="tokens_visitante")
    accesos = relationship("Acceso", back_populates="visitante")
