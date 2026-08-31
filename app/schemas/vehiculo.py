from pydantic import BaseModel
from typing import Optional

class VehiculoBase(BaseModel):
    patente: str
    descripcion: Optional[str] = None

class VehiculoCreate(VehiculoBase):
    pass

class VehiculoResponse(VehiculoBase):
    id: int
    activo: bool
    residente_id: int
    model_config = {"from_attributes": True}
