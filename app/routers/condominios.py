from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.condominio import Condominio
from app.schemas.condominio import CondominioCreate, CondominioResponse

router = APIRouter(
    prefix="/condominios",
    tags=["Condominios"]
)

@router.get("/", response_model=list[CondominioResponse])
async def listar_condominios(db: Session = Depends(get_db)):
    return db.query(Condominio).all()

@router.get("/{condominio_id}", response_model=CondominioResponse)
async def obtener_condominio(condominio_id: int, db: Session = Depends(get_db)):
    condominio = db.query(Condominio).filter(Condominio.id == condominio_id).first()
    if not condominio:
        raise HTTPException(status_code=404, detail="Condominio no encontrado")
    return condominio

@router.post("/", response_model=CondominioResponse)
async def crear_condominio(condominio: CondominioCreate, db: Session = Depends(get_db)):
    nuevo = Condominio(
        nombre=condominio.nombre,
        direccion=condominio.direccion,
        plan=condominio.plan or "basico"
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.delete("/{condominio_id}")
async def desactivar_condominio(condominio_id: int, db: Session = Depends(get_db)):
    condominio = db.query(Condominio).filter(Condominio.id == condominio_id).first()
    if not condominio:
        raise HTTPException(status_code=404, detail="Condominio no encontrado")
    condominio.activo = False
    db.commit()
    return {"mensaje": "Condominio desactivado"}
