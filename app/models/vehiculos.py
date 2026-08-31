from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class Vehiculo(Base):
    __tablename__ = "vehiculos"
    id= Column(Integer, primary_key = True, index= True)
    patente= Column(String, unique=True ,nullable=False, index = True)
    descripcion= Column(String, nullable=False)
    activo = Column(Boolean, default= True)
    creado_en = Column(DateTime, default = lambda: datetime.now(timezone.utc))

    residente_id = Column(Integer, ForeignKey("residentes.id") ,nullable=False)

    residente = relationship("Residente", back_populates="vehiculos")
    accesos = relationship("Acceso", back_populates="vehiculo")