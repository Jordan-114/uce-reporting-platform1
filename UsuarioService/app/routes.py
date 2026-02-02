import os
from app.auth.auth_handler import verify_password

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao import usuario_dao
from app.dto_usuario import UsuarioCreate, Usuario, LoginData, UsuarioDTO
from app.database import get_db
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import create_access_token

router = APIRouter()

MODO_DEMO = os.getenv("MODO_DEMO", "false").lower() == "true"

# -------------------------
# REGISTRO
# -------------------------
@router.post("/registro", response_model=Usuario)
async def registrar_usuario(usuario: UsuarioCreate, db: AsyncSession = Depends(get_db)):
    if MODO_DEMO:
        raise HTTPException(status_code=503, detail="Modo demo activo")

    db_usuario = await usuario_dao.get_usuario_por_correo(db, correo=usuario.correo)
    if db_usuario:
        raise HTTPException(status_code=400, detail="Correo ya registrado")
    return await usuario_dao.create_usuario(db, usuario)

# -------------------------
# LOGIN
# -------------------------
@router.post("/login")
async def login(data: LoginData, db: AsyncSession = Depends(get_db)):
    if MODO_DEMO:
        return {
            "access_token": "demo-token",
            "token_type": "bearer",
            "rol": "admin"
        }

    usuario = await usuario_dao.get_usuario_por_correo(db, data.correo)

    if not usuario:
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")

    # 🔐 VALIDAR CONTRASEÑA (AQUÍ ESTABA EL PROBLEMA)
    if not verify_password(data.pssw, usuario.password):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")

    token = create_access_token(
        id_usuario=usuario.id_usuario,
        nombre=usuario.nombre,
        email=usuario.correo,
        role=usuario.rol
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "rol": usuario.rol
    }

# -------------------------
# USUARIOS (CRÍTICO)
# -------------------------
@router.get("/usuarios", response_model=List[UsuarioDTO])
async def listar_usuarios(db: AsyncSession = Depends(get_db)):
    if MODO_DEMO:
        return []

    return await usuario_dao.get_todos_los_usuarios(db)

# -------------------------
# RUTA PROTEGIDA
# -------------------------
@router.get("/protegida", dependencies=[Depends(JWTBearer())])
async def ruta_protegida():
    return {"mensaje": "Acceso permitido"}
