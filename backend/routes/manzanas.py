from fastapi import APIRouter, HTTPException
from config.db import conn
from models.models import manzanas
from schemas.schemas import Manzana

router = APIRouter(
    prefix="/manzanas",
    tags=["manzana"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
async def create_manzana(manzana: Manzana):
    if conn.execute(manzanas.select().where(manzanas.c.nombre == manzana.nombre)).first():
        raise HTTPException(status_code=404, detail="La manzana ya existe")
    nueva_manzana = Manzana.manzana_schema_db(manzana)
    result = conn.execute(manzanas.insert().values(nueva_manzana))
    conn.commit()
    return Manzana.manzana_schema(conn.execute(manzanas.select().where(manzanas.c.id == result.lastrowid)).first())

@router.get("/")
async def get_manzanas():
    return Manzana.manzanas_schema(conn.execute(manzanas.select().order_by(manzanas.c.nombre)).fetchall())

@router.get("/{id}")
async def get_manzana(id: int):
    manzana = conn.execute(manzanas.select().where(manzanas.c.id == id)).first()
    if not manzana:
        raise HTTPException(status_code=404, detail="Manzana no encontrada")
    return Manzana.manzana_schema(manzana)