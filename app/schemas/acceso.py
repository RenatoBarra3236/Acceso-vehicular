from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class TipoAcceso(str, Enum):
    entrada = "entrada"
    salida = "salida"

class MetodoAcceso(str, Enum):
    BLE = "BLE"
    PIN = "PIN"
    QR = "QR"
    manual = "manual"

class AccesoCreate(BaseModel):
    tipo: TipoAcceso
    metodo_acceso: MetodoAcceso
    vehiculo_id: Optional[int] = None
    visitante_id: Optional[int] = None

class AccesoResponse(BaseModel):
    id: int
    tipo: str
    metodo_acceso: str
    timestamp: datetime
    vehiculo_id: Optional[int]
    visitante_id: Optional[int]
    model_config = {"from_attributes": True}
