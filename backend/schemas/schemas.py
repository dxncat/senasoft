from pydantic import BaseModel
from config.db import conn
from models import models

class Municipio(BaseModel):
    id: int | None = None
    nombre: str

    def municipio_schema(municipio) -> dict:
        return {
            "id": municipio.id,
            "nombre": municipio.nombre
        }
    
    def municipios_schema(municipios) -> list:
        return [Municipio.municipio_schema(municipio) for municipio in municipios]

class Manzana(BaseModel):
    id: int | None = None
    nombre: str
    localidad: str
    direccion: str
    municipio_id: int

    def manzana_schema_db(manzana) -> dict:
        return{
            "id": manzana.id,
            "nombre": manzana.nombre,
            "localidad": manzana.localidad,
            "direccion": manzana.direccion,
            "municipio_id": manzana.municipio_id
        }

    def manzana_schema(manzana) -> dict:
        municipio = Municipio.municipio_schema(conn.execute(models.municipios.select().where(models.municipios.c.id == manzana.municipio_id)).first())
        return {
            "id": manzana.id,
            "nombre": manzana.nombre,
            "localidad": manzana.localidad,
            "direccion": manzana.direccion,
            "municipio": municipio
        }
    
    def manzanas_schema(manzanas) -> list:
        return [Manzana.manzana_schema(manzana) for manzana in manzanas]

class Establecimiento(BaseModel):
    id: int | None = None
    nombre: str
    responsable: str
    direccion: str

    def establecimiento_schema_db(establecimiento) -> dict:
        return {
            "id": establecimiento.id,
            "nombre": establecimiento.nombre,
            "responsable": establecimiento.responsable,
            "direccion": establecimiento.direccion
        }

    def establecimiento_schema(establecimiento) -> dict:
        return {
            "id": establecimiento.id,
            "nombre": establecimiento.nombre,
            "responsable": establecimiento.responsable,
            "direccion": establecimiento.direccion
        }
    
    def establecimientos_schema(establecimientos) -> list:
        return [Establecimiento.establecimiento_schema(establecimiento) for establecimiento in establecimientos]

class Servicio(BaseModel):
    id: int | None = None
    nombre: str
    descripcion: str
    categoria: str
    manzana_id: int
    establecimiento_id: int

    def servicio_schema_db(servicio) -> dict:
        return {
            "id": servicio.id,
            "nombre": servicio.nombre,
            "descripcion": servicio.descripcion,
            "categoria": servicio.categoria,
            "manzana_id": servicio.manzana_id,
            "establecimiento_id": servicio.establecimiento_id
        }

    def servicio_schema(servicio) -> dict:
        manzana = Manzana.manzana_schema(conn.execute(models.manzanas.select().where(models.manzanas.c.id == servicio.manzana_id)).first())
        establecimiento = Establecimiento.establecimiento_schema(conn.execute(models.establecimientos.select().where(models.establecimientos.c.id == servicio.establecimiento_id)).first())
        return {
            "id": servicio.id,
            "nombre": servicio.nombre,
            "descripcion": servicio.descripcion,
            "categoria": servicio.categoria,
            "manzana": manzana,
            "establecimiento": establecimiento
        }
    
    def servicios_schema(servicios) -> list:
        return [Servicio.servicio_schema(servicio) for servicio in servicios]


class Mujer(BaseModel):
    id: int | None = None
    tipo_documento: str
    documento: int
    nombre: str
    apellido: str
    telefono: int
    correo: str
    contrasena: str
    ciudad: str
    direccion: str
    servicio_id: int

    def mujer_schema_db(mujer) -> dict:
        return {
            "id": mujer.id,
            "tipo_documento": mujer.tipo_documento,
            "documento": mujer.documento,
            "nombre": mujer.nombre,
            "apellido": mujer.apellido,
            "telefono": mujer.telefono,
            "correo": mujer.correo,
            "contrasena": mujer.contrasena,
            "ciudad": mujer.ciudad,
            "direccion": mujer.direccion,
            "servicio_id": mujer.servicio_id
        }

    def mujer_schema(mujer) -> dict:
        servicio = Servicio.servicio_schema(conn.execute(models.servicios.select().where(models.servicios.c.id == mujer.servicio_id)).first())
        return {
            "id": mujer.id,
            "tipo_documento": mujer.tipo_documento,
            "documento": mujer.documento,
            "nombre": mujer.nombre,
            "apellido": mujer.apellido,
            "telefono": mujer.telefono,
            "correo": mujer.correo,
            "contrasena": mujer.contrasena if mujer.contrasena else None,
            "ciudad": mujer.ciudad,
            "direccion": mujer.direccion,
            "servicio": servicio
        }
    
    def mujeres_schema(mujeres) -> list:
        return [Mujer.mujer_schema(mujer) for mujer in mujeres]

class Agenda(BaseModel):
    id: int | None = None
    fecha: str
    hora: str
    manzana_id: int
    servicio_id: int
    mujer_id: int

    def agenda_schema_db(agenda) -> dict:
        return {
            "id": agenda.id,
            "fecha": agenda.fecha,
            "hora": agenda.hora,
            "manzana_id": agenda.manzana_id,
            "servicio_id": agenda.servicio_id,
            "mujer_id": agenda.mujer_id
        }

    def agenda_schema(agenda) -> dict:
        manzana = Manzana.manzana_schema(conn.execute(models.manzanas.select().where(models.manzanas.c.id == agenda.manzana_id)).first())
        servicio = Servicio.servicio_schema(conn.execute(models.servicios.select().where(models.servicios.c.id == agenda.servicio_id)).first())
        mujer = Mujer.mujer_schema(conn.execute(models.mujeres.select().where(models.mujeres.c.id == agenda.mujer_id)))
        return {
            "id": agenda.id,
            "fecha": agenda.fecha,
            "hora": agenda.hora,
            "manzana": manzana,
            "servicio": servicio,
            "mujer": mujer
        }
    
    def agendas_schema(agendas) -> list:
        return [Agenda.agenda_schema(agenda) for agenda in agendas]