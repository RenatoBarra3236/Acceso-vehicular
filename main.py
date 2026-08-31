from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import residentes, vehiculos, condominios, visitantes, accesos
from app.routers import auth
from app import models

app = FastAPI(
    title="Sistema de Acceso Condominio",
    version="0.2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crea todas las tablas al arrancar
Base.metadata.create_all(bind=engine)

# Routers
app.include_router(auth.router)
app.include_router(condominios.router)
app.include_router(residentes.router)
app.include_router(vehiculos.router)
app.include_router(visitantes.router)
app.include_router(accesos.router)


@app.get("/")
async def raiz():
    return {"mensaje": "Sistema de Acceso Condominio v0.2.0"}