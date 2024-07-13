import jwt
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from config.db import conn
from models.models import mujeres
from schemas.schemas import Mujer
from decouple import config
from datetime import datetime, timedelta
from auth.auth import mujer_actual

router = APIRouter(
    prefix="/mujeres",
    tags=["mujer"],
    responses={404: {"description": "Not found"}},
)

crypt_context = CryptContext(
        schemes=["bcrypt"],
        deprecated="auto"
    )

ALGORITHM = config("ALGORITHM")
SECRET_KEY = config("SECRET_KEY")
ACCESS_TOKEN_DURATION = 4

@router.get("/")
async def get_mujeres():
    return Mujer.mujeres_schema(conn.execute(mujeres.select().order_by(mujeres.c.nombre)).fetchall())

@router.get("/info/{id}")
async def get_mujer(id: int):
    mujer = conn.execute(mujeres.select().where(mujeres.c.id == id)).first()
    if not mujer:
        raise HTTPException(status_code=404, detail="Mujer no encontrada")
    return Mujer.mujer_schema(mujer)

@router.post("/registro")
async def create_mujeres(mujer: Mujer):
    if conn.execute(mujeres.select().where(mujeres.c.correo == mujer.correo)).first():
        raise HTTPException(status_code=404, detail="El correo ya existe")
    if conn.execute(mujeres.select().where(mujeres.c.documento == mujer.documento)).first():
        raise HTTPException(status_code=404, detail="El documento ya existe")
    nueva_mujer = Mujer.mujer_schema_db(mujer)
    nueva_mujer["contrasena"] = crypt_context.hash(nueva_mujer["contrasena"])
    result = conn.execute(mujeres.insert().values(nueva_mujer))
    conn.commit()
    print(Mujer.mujer_schema(conn.execute(mujeres.select().where(mujeres.c.id == result.lastrowid)).first()))
    access_token = jwt.encode(
        {
            "sub": mujer.documento,
            "exp": datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_DURATION)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/acceso")
async def login_mujeres(form: OAuth2PasswordRequestForm = Depends()):
    mujer_f = conn.execute(mujeres.select().where(mujeres.c.documento == form.username)).first()
    if not mujer_f:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    mujer = Mujer.mujer_schema_db(mujer_f)
    if not crypt_context.verify(form.password, mujer["contrasena"]):
        raise HTTPException(status_code=404, detail="Contraseña incorrecta")
    access_token = jwt.encode(
        {
            "sub": mujer["documento"],
            "exp": datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_DURATION)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.put("/actualizar")
async def update_password(new_password: str, mujer: Mujer = Depends(mujer_actual)):
    mujer['contrasena'] = crypt_context.hash(new_password)
    conn.execute(mujeres.update().where(mujeres.c.id == mujer['id']).values(contrasena=mujer['contrasena']))
    conn.commit()
    return {"message": "Contraseña actualizada exitosamente"}

@router.get("/me")
async def read_users_me(user: Mujer = Depends(mujer_actual)):
    return user