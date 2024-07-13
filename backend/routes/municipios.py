from fastapi import APIRouter, HTTPException
from config.db import conn
from models.models import municipios
from schemas.schemas import Municipio

router = APIRouter(
    prefix="/municipios",
    tags=["municipio"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
async def create_municipio(municipio: Municipio):
    if conn.execute(municipios.select().where(municipios.c.nombre == municipio.nombre)).first():
        raise HTTPException(status_code=404, detail="El municipio ya existe")
    nuevo_municipio = Municipio.municipio_schema(municipio)
    result = conn.execute(municipios.insert().values(nuevo_municipio))
    conn.commit()
    return Municipio.municipio_schema(conn.execute(municipios.select().where(municipios.c.id == result.lastrowid)).first())

@router.get("/")
async def get_municipio():
    return Municipio.municipios_schema(conn.execute(municipios.select().order_by(municipios.c.nombre)).fetchall())

@router.get("/{id}")
async def get_municipio(id: int):
    municipio = conn.execute(municipios.select().where(municipios.c.id == id)).first()
    if not municipio:
        raise HTTPException(status_code=404, detail="Municipio no encontrado")
    return Municipio.municipio_schema()
        