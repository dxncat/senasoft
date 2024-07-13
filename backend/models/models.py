from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Time, Date
from config.db import meta, engine

municipios = Table(
    "municipios",
    meta,
    Column("id", Integer, primary_key=True),
    Column("nombre", String(255), nullable=False),
)

manzanas = Table(
    "manzanas",
    meta,
    Column("id", Integer, primary_key=True),
    Column("nombre", String(255), nullable=False),
    Column("localidad", String(255), nullable=False),
    Column("direccion", String(255), nullable=False),
    Column("municipio_id", Integer, ForeignKey("municipios.id"), nullable=False)
)

servicios = Table(
    "servicios",
    meta,
    Column("id", Integer, primary_key=True),
    Column("nombre", String(255), nullable=False),
    Column("descripcion", String(255), nullable=False),
    Column("categoria", String(255), nullable=False),
    Column("manzana_id", Integer, ForeignKey("manzanas.id"), nullable=False),
    Column("establecimiento_id", Integer, ForeignKey("establecimientos.id"), nullable=False)
)

establecimientos = Table(
    "establecimientos",
    meta,
    Column("id", Integer, primary_key=True),
    Column("nombre", String(255), nullable=False),
    Column("responsable", String(255), nullable=False),
    Column("direccion", String(255), nullable=False),
)

mujeres = Table(
    "mujeres",
    meta,
    Column("id", Integer, primary_key=True),
    Column("tipo_documento", String(255), nullable=False),
    Column("documento", Integer, nullable=False),
    Column("nombre", String(255), nullable=False),
    Column("apellido", String(255), nullable=False),
    Column("telefono", Integer, nullable=False),
    Column("correo", String(255), nullable=False),
    Column("contrasena", String(255), nullable=False),
    Column("ciudad", String(255), nullable=False),
    Column("direccion", String(255), nullable=False),
    Column("servicio_id", Integer, ForeignKey("servicios.id"), nullable=False)
)

agendas = Table(
    "agendas",
    meta,
    Column("id", Integer, primary_key=True),
    Column("fecha", Date, nullable=False),
    Column("hora", Time, nullable=False),
    Column("manzana_id", Integer, ForeignKey("manzanas.id"), nullable=False),
    Column("servicio_id", Integer, ForeignKey("servicios.id"), nullable=False),
    Column("mujer_id", Integer, ForeignKey("mujeres.id"), nullable=False)
)

meta.create_all(engine)