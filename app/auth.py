from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.residentes import Residente

# Clave secreta para firmar los tokens
# En producción esto debe estar en una variable de entorno
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# Contexto para hashear y verificar contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Le dice a FastAPI dónde esperar el token en los requests
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# ── Funciones de contraseña ──────────────────────────────

def hashear_password(password: str) -> str:
    return pwd_context.hash(password)

def verificar_password(password_plano: str, password_hasheado: str) -> bool:
    return pwd_context.verify(password_plano, password_hasheado)


# ── Funciones de token ───────────────────────────────────

def crear_token(data: dict) -> str:
    payload = data.copy()
    expiracion = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expiracion})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# ── Dependencia: obtener residente autenticado ───────────

def get_residente_actual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Residente:
    credenciales_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credenciales_invalidas
    except JWTError:
        raise credenciales_invalidas

    residente = db.query(Residente).filter(Residente.email == email).first()
    if residente is None:
        raise credenciales_invalidas
    return residente


# ── Dependencia: solo administradores ───────────────────

def solo_admin(residente: Residente = Depends(get_residente_actual)) -> Residente:
    if residente.rol != "administrador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requiere rol de administrador"
        )
    return residente