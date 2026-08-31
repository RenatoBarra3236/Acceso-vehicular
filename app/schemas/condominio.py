from pydantic import BaseModel
from typing import Optional

class CondominioCreate(BaseModel):
    nombre: str
    direccion: str
    plan: Optional[str] = "basico"

class CondominioResponse(BaseModel):
    id: int
    nombre: str
    direccion: str
    plan: str
    activo: bool
    model_config = {"from_attributes": True}
