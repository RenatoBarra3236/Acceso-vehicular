from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from secrets import token_urlsafe
from app.database import get_db
from app.models.residentes import Residente
from app.models.visitante import Visitante
from app.schemas.visitante import VisitanteCreate, VisitanteResponse

router = APIRouter(
    prefix="/visitantes",
    tags=["Visitantes"]
)

@router.post("/", response_model=VisitanteResponse)
async def crear_token_visitante(datos: VisitanteCreate, db: Session = Depends(get_db)):
    residente = db.query(Residente).filter(
        Residente.id == datos.creado_por_id,
        Residente.activo == True
    ).first()
    if not residente:
        raise HTTPException(status_code=404, detail="Residente no encontrado")

    if datos.valido_hasta <= datos.valido_desde:
        raise HTTPException(status_code=400, detail="valido_hasta debe ser posterior a valido_desde")

    visitante = Visitante(
        token_acceso=token_urlsafe(32),
        nombre=datos.nombre,
        creado_por_id=datos.creado_por_id,
        valido_desde=datos.valido_desde,
        valido_hasta=datos.valido_hasta,
        usos_maximos=datos.usos_maximos,
    )
    db.add(visitante)
    db.commit()
    db.refresh(visitante)
    return visitante

@router.get("/residente/{residente_id}", response_model=list[VisitanteResponse])
async def listar_tokens_residente(residente_id: int, db: Session = Depends(get_db)):
    residente = db.query(Residente).filter(Residente.id == residente_id).first()
    if not residente:
        raise HTTPException(status_code=404, detail="Residente no encontrado")
    return db.query(Visitante).filter(Visitante.creado_por_id == residente_id).all()

@router.delete("/{visitante_id}/revocar")
async def revocar_token(visitante_id: int, db: Session = Depends(get_db)):
    visitante = db.query(Visitante).filter(Visitante.id == visitante_id).first()
    if not visitante:
        raise HTTPException(status_code=404, detail="Token no encontrado")
    visitante.revocado = True
    db.commit()
    return {"mensaje": "Token revocado"}

@router.get("/validar/{token}")
async def validar_token(token: str, db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    visitante = db.query(Visitante).filter(Visitante.token_acceso == token).first()
    if not visitante:
        raise HTTPException(status_code=404, detail="Token no encontrado")
    if visitante.revocado:
        raise HTTPException(status_code=403, detail="Token revocado")
    if now < visitante.valido_desde or now > visitante.valido_hasta:
        raise HTTPException(status_code=403, detail="Token fuera de periodo de validez")
    if visitante.usos_actuales >= visitante.usos_maximos:
        raise HTTPException(status_code=403, detail="Token sin usos restantes")
    return {"valido": True, "usos_restantes": visitante.usos_maximos - visitante.usos_actuales}
