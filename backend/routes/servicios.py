from fastapi import APIRouter, HTTPException
from config.db import conn
from models.models import servicios
from schemas.schemas import Servicio

router = APIRouter(
    prefix="/servicios",
    tags=["servicio"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
async def create_servicio(servicio: Servicio):
    nuevo_servicio = Servicio.servicio_schema_db(servicio)
    result = conn.execute(servicios.insert().values(nuevo_servicio))
    conn.commit()
    return Servicio.servicio_schema(conn.execute(servicios.select().where(servicios.c.id == result.lastrowid)).first())

@router.get("/")
async def get_servicios():
    return Servicio.servicios_schema(conn.execute(servicios.select().order_by(servicios.c.nombre)).fetchall())

@router.get("/{id}")
async def get_servicio(id: int):
    servicio = conn.execute(servicios.select().where(servicios.c.id == id)).first()
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return Servicio.servicio_schema(servicio)