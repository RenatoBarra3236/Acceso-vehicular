from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class VisitanteCreate(BaseModel):
    nombre: Optional[str] = None
    creado_por_id: int
    valido_desde: datetime
    valido_hasta: datetime
    usos_maximos: int = 1

class VisitanteResponse(BaseModel):
    id: int
    token_acceso: str
    nombre: Optional[str]
    creado_por_id: int
    valido_desde: datetime
    valido_hasta: datetime
    usos_maximos: int
    usos_actuales: int
    revocado: bool
    model_config = {"from_attributes": True}
