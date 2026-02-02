from fastapi import APIRouter, HTTPException, Header

from app.abstract_factory_quejas import (
    QuejaFactoryCombinada,
    QuejaFactoryMongo,
    QuejaFactoryPostgre
)
from app.abstract_factory_usuario import UsuarioFactory
from app.polling import obtener_cache_web_por_usuario

router = APIRouter()

# -----------------------------
# Reporte combinado (web + oficina)
# -----------------------------
@router.get("/api/reporte/combinado")
async def obtener_reporte_combinado():
    factory = QuejaFactoryCombinada()
    return await factory.obtener_quejas()

# -----------------------------
# Reporte solo quejas web (Mongo)
# -----------------------------
@router.get("/api/reporte/web")
async def obtener_reporte_web():
    factory = QuejaFactoryMongo()
    return await factory.obtener_quejas()

# -----------------------------
# Reporte solo quejas oficina (Postgre)
# -----------------------------
@router.get("/api/reporte/oficina")
async def obtener_reporte_oficina():
    factory = QuejaFactoryPostgre()
    return await factory.obtener_quejas()

# -----------------------------
# Reporte de quejas web por usuario
# -----------------------------
@router.get("/api/reporte/web/usuario/{id_usuario}")
async def obtener_quejas_usuario(
    id_usuario: str,
    authorization: str = Header(None)
):
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Token de autorización no proporcionado"
        )

    # Bearer <token>
    token = authorization.split(" ")[1]

    quejas = await obtener_cache_web_por_usuario(id_usuario)
    return {"quejas": quejas}

# -----------------------------
# Obtener usuarios (admin)
# -----------------------------
@router.get("/api/reporte/usuarios")
async def obtener_usuarios_para_admin():
    factory = UsuarioFactory()
    return await factory.obtener_usuarios()
