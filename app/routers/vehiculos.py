from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.residentes import Residente
from app.models.vehiculos import Vehiculo
from app.schemas.vehiculo import VehiculoCreate, VehiculoResponse

router = APIRouter(
    prefix= "/vehiculos", 
    tags= ["Vehiculos"]
)

@router.get("/", response_model=list[VehiculoResponse])
async def listar_vehiculos(db: Session = Depends(get_db)):
    return db.query(Vehiculo).all()

@router.get('/{vehiculo_id}', response_model = VehiculoResponse)
async def obtener_vehiculo(vehiculo_id: int, db: Session = Depends(get_db)):
    vehiculo = db.query(Vehiculo).filter(Vehiculo.id == vehiculo_id).first()
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehiculo no encontrado")
    return vehiculo

@router.post("/residente/{residente_id}", response_model = VehiculoResponse)
async def agregar_vehiculo(residente_id: int, vehiculo: VehiculoCreate, db: Session = Depends(get_db)):
    residente = db.query(Residente).filter(Residente.id == residente_id).first()
    if not residente:
        raise HTTPException(status_code=404, detail="Residente no encontrado")
    
    existe = db.query(Vehiculo).filter(Vehiculo.patente == vehiculo.patente).first()
    if existe:
        raise HTTPException(status_code=400, detail="La patente ya esta registrada")
    
    nuevo_vehiculo = Vehiculo(
        patente = vehiculo.patente,
        descripcion = vehiculo.descripcion,
        activo = True,
        residente_id = residente_id
    )
    db.add(nuevo_vehiculo)
    db.commit()
    db.refresh(nuevo_vehiculo)
    return nuevo_vehiculo

@router.delete("/{vehiculo_id}")
async def desactivar_vehiculo(vehiculo_id: int, db: Session = Depends(get_db)):
    vehiculo = db.query(Vehiculo).filter(Vehiculo.id == vehiculo_id).first()
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehiculo no encontrado")
    vehiculo.activo = False
    db.commit()
    return {"mensaje": "Vehiculo desactivado"}