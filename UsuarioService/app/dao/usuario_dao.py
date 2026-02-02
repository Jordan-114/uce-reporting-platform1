from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Usuario
from app.auth.auth_handler import get_password_hash, verify_password

# -------------------------
# OBTENER USUARIO POR CORREO
# -------------------------
async def get_usuario_por_correo(db: AsyncSession, correo: str):
    result = await db.execute(
        select(Usuario).where(Usuario.correo == correo)
    )
    return result.scalar_one_or_none()

# -------------------------
# CREAR USUARIO (FIX AQUÍ)
# -------------------------
async def create_usuario(db: AsyncSession, usuario):
    hashed_password = get_password_hash(usuario.pssw)

    nuevo_usuario = Usuario(
        nombre=usuario.nombre,
        correo=usuario.correo,
        password=hashed_password,  # ✅ CAMBIO CLAVE
        rol=usuario.rol if usuario.rol in ["cliente", "empleado", "admin"] else "cliente"
    )

    db.add(nuevo_usuario)
    await db.commit()
    await db.refresh(nuevo_usuario)
    return nuevo_usuario

# -------------------------
# LISTAR USUARIOS
# -------------------------
async def get_todos_los_usuarios(db: AsyncSession):
    result = await db.execute(select(Usuario))
    return result.scalars().all()
