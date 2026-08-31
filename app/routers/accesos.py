from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.database import get_db
from app.models.acceso import Acceso
from app.models.vehiculos import Vehiculo
from app.models.visitante import Visitante
from app.schemas.acceso import AccesoCreate, AccesoResponse

router = APIRouter(
    prefix="/accesos",
    tags=["Accesos"]
)

@router.post("/", response_model=AccesoResponse)
async def registrar_acceso(datos: AccesoCreate, db: Session = Depends(get_db)):
    if not datos.vehiculo_id and not datos.visitante_id:
        raise HTTPException(status_code=400, detail="Se requiere vehiculo_id o visitante_id")

    if datos.vehiculo_id:
        vehiculo = db.query(Vehiculo).filter(
            Vehiculo.id == datos.vehiculo_id,
            Vehiculo.activo == True
        ).first()
        if not vehiculo:
            raise HTTPException(status_code=404, detail="Vehiculo no encontrado o inactivo")

    if datos.visitante_id:
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        visitante = db.query(Visitante).filter(Visitante.id == datos.visitante_id).first()
        if not visitante:
            raise HTTPException(status_code=404, detail="Token de visitante no encontrado")
        if visitante.revocado:
            raise HTTPException(status_code=403, detail="Token de visitante revocado")
        if now < visitante.valido_desde or now > visitante.valido_hasta:
            raise HTTPException(status_code=403, detail="Token de visitante expirado")
        if visitante.usos_actuales >= visitante.usos_maximos:
            raise HTTPException(status_code=403, detail="Token de visitante sin usos restantes")
        visitante.usos_actuales += 1

    acceso = Acceso(
        tipo=datos.tipo,
        metodo_acceso=datos.metodo_acceso,
        vehiculo_id=datos.vehiculo_id,
        visitante_id=datos.visitante_id,
    )
    db.add(acceso)
    db.commit()
    db.refresh(acceso)
    return acceso

@router.get("/", response_model=list[AccesoResponse])
async def listar_accesos(db: Session = Depends(get_db)):
    return db.query(Acceso).order_by(Acceso.timestamp.desc()).all()

@router.get("/vehiculo/{vehiculo_id}", response_model=list[AccesoResponse])
async def accesos_por_vehiculo(vehiculo_id: int, db: Session = Depends(get_db)):
    vehiculo = db.query(Vehiculo).filter(Vehiculo.id == vehiculo_id).first()
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehiculo no encontrado")
    return db.query(Acceso).filter(
        Acceso.vehiculo_id == vehiculo_id
    ).order_by(Acceso.timestamp.desc()).all()
