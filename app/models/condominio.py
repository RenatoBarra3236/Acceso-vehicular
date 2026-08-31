from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class Condominio(Base):
    __tablename__ = "condominios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    direccion = Column(String, nullable=False)
    plan = Column(String, default="basico")  # basico / pro
    activo = Column(Boolean, default=True)
    creado_en = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    residentes = relationship("Residente", back_populates="condominio")
