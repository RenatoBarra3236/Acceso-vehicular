from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.residentes import Residente
from app.models.condominio import Condominio
from app.schemas.residentes import ResidenteCreate
from app.auth import verificar_password, crear_token, hashear_password, get_residente_actual

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    residente = db.query(Residente).filter(Residente.email == form_data.username).first()

    if not residente or not verificar_password(form_data.password, residente.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not residente.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cuenta desactivada"
        )

    token = crear_token({
        "sub": residente.email,
        "rol": residente.rol,
        "condominio_id": residente.condominio_id
    })

    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
async def mi_perfil(residente: Residente = Depends(get_residente_actual)):
    return {
        "id": residente.id,
        "nombre": residente.nombre,
        "email": residente.email,
        "rol": residente.rol,
        "condominio_id": residente.condominio_id,
        "activo": residente.activo
    }


@router.post("/registro-inicial")
async def registro_inicial(
    residente: ResidenteCreate,
    db: Session = Depends(get_db)
):
    # Verificar que el condominio existe
    condominio = db.query(Condominio).filter(Condominio.id == residente.condominio_id).first()
    if not condominio:
        raise HTTPException(status_code=404, detail="Condominio no encontrado")

    # Verificar que no exista ningún admin en ese condominio
    admin_existe = db.query(Residente).filter(
        Residente.condominio_id == residente.condominio_id,
        Residente.rol == "administrador"
    ).first()
    if admin_existe:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un administrador en este condominio"
        )

    nuevo = Residente(
        nombre=residente.nombre,
        email=residente.email,
        hashed_password=hashear_password(residente.password),
        pin=residente.pin,
        rol="administrador",
        condominio_id=residente.condominio_id,
        activo=True
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return {"mensaje": "Administrador creado correctamente", "id": nuevo.id}