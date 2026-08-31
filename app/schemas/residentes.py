from pydantic import BaseModel
from typing import Optional
from app.schemas.vehiculo import VehiculoResponse

class ResidenteCreate(BaseModel):
    nombre: str
    email: str
    password: str
    condominio_id: int
    pin: Optional[str] = None
    rol: Optional[str] = "residente"  # por defecto residente, puede ser "administrador"

class ResidenteResponse(BaseModel):
    id: int
    nombre: str
    email: str
    activo: bool
    rol: str
    condominio_id: int
    vehiculos: list[VehiculoResponse] = []
    model_config = {"from_attributes": True}
