from fastapi import APIRouter, HTTPException, Depends
from config.db import conn
from models.models import agendas
from schemas.schemas import Agenda, Mujer
from auth.auth import mujer_actual

router = APIRouter(
    prefix="/agendas",
    tags=["agenda"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
async def create_agenda(agenda: Agenda, mujer: Mujer = Depends(mujer_actual)):
    nueva_agenda = {"fecha": agenda.fecha, "hora": agenda.hora, "manzana_id": agenda.manzana_id, "servicio_id": mujer.servicio_id, "mujer_id": mujer.id}
    result = conn.execute(agendas.insert().values(nueva_agenda))
    conn.commit()
    return Agenda.agenda_schema(conn.execute(agendas.select().where(agendas.c.id == result.lastrowid)).first())

@router.get("/")
async def get_agendas(mujer: Mujer = Depends(mujer_actual)):
    return [Agenda.agenda_schema(agenda) for agenda in conn.execute(agendas.select().where(agendas.c.mujer_id == mujer.id)).fetchall()]