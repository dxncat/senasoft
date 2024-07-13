from fastapi import APIRouter, HTTPException
from config.db import conn
from models.models import establecimientos
from schemas.schemas import Establecimiento

router = APIRouter(
    prefix="/establecimientos",
    tags=["establecimiento"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
async def create_establecimiento(establecimiento: Establecimiento):
    if conn.execute(establecimientos.select().where(establecimientos.c.nombre == establecimiento.nombre)).first():
        raise HTTPException(status_code=404, detail="El establecimiento ya existe")
    nuevo_establecimiento = Establecimiento.establecimiento_schema_db(establecimiento)
    result = conn.execute(establecimientos.insert().values(nuevo_establecimiento))
    conn.commit()
    return Establecimiento.establecimiento_schema(conn.execute(establecimientos.select().where(establecimientos.c.id == result.lastrowid)).first())

@router.get("/")
async def get_establecimientos():
    return Establecimiento.establecimientos_schema(conn.execute(establecimientos.select().order_by(establecimientos.c.nombre)).fetchall())

@router.get("/{id}")
async def get_establecimiento(id: int):
    establecimiento = conn.execute(establecimientos.select().where(establecimientos.c.id == id)).first()
    if not establecimiento:
        raise HTTPException(status_code=404, detail="Establecimiento no encontrado")
    return Establecimiento.establecimiento_schema(establecimiento)

@router.get("/{servicio_id}")
async def get_establecimiento_servicio_id(servicio_id: int):
    return Establecimiento.establecimientos_schema(conn.execute(establecimientos.select().where(establecimientos.c.servicio_id == servicio_id)).fetchall())