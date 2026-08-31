from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.residentes import Residente
from app.models.condominio import Condominio
from app.schemas.residentes import ResidenteCreate, ResidenteResponse
from app.auth import hashear_password, get_residente_actual, solo_admin

router = APIRouter(
    prefix="/residentes",
    tags=["Residentes"]
)


@router.get("/", response_model=list[ResidenteResponse])
async def listar_residentes(
    db: Session = Depends(get_db),
    residente_actual: Residente = Depends(get_residente_actual)
):
    # Admin ve todos los residentes de su condominio
    # Residente solo se ve a sí mismo
    if residente_actual.rol == "administrador":
        return db.query(Residente).filter(
            Residente.condominio_id == residente_actual.condominio_id
        ).all()
    return [residente_actual]


@router.get("/me", response_model=ResidenteResponse)
async def mi_perfil(residente_actual: Residente = Depends(get_residente_actual)):
    return residente_actual


@router.get("/{residente_id}", response_model=ResidenteResponse)
async def obtener_residente(
    residente_id: int,
    db: Session = Depends(get_db),
    residente_actual: Residente = Depends(get_residente_actual)
):
    residente = db.query(Residente).filter(Residente.id == residente_id).first()
    if not residente:
        raise HTTPException(status_code=404, detail="Residente no encontrado")

    # Solo puede ver residentes de su mismo condominio
    if residente.condominio_id != residente_actual.condominio_id:
        raise HTTPException(status_code=403, detail="Acceso denegado")

    return residente


@router.post("/", response_model=ResidenteResponse)
async def crear_residente(
    residente: ResidenteCreate,
    db: Session = Depends(get_db),
    _: Residente = Depends(solo_admin)  # solo admins pueden crear residentes
):
    # Verificar que el condominio existe
    condominio = db.query(Condominio).filter(Condominio.id == residente.condominio_id).first()
    if not condominio:
        raise HTTPException(status_code=404, detail="Condominio no encontrado")

    # Verificar email único
    if db.query(Residente).filter(Residente.email == residente.email).first():
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    nuevo = Residente(
        nombre=residente.nombre,
        email=residente.email,
        hashed_password=hashear_password(residente.password),  # hashea aquí
        pin=residente.pin,
        rol=residente.rol or "residente",
        condominio_id=residente.condominio_id,
        activo=True
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.delete("/{residente_id}")
async def desactivar_residente(
    residente_id: int,
    db: Session = Depends(get_db),
    _: Residente = Depends(solo_admin)
):
    residente = db.query(Residente).filter(Residente.id == residente_id).first()
    if not residente:
        raise HTTPException(status_code=404, detail="Residente no encontrado")

    residente.activo = False
    db.commit()
    return {"mensaje": "Residente desactivado correctamente"}