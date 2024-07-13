import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from config.db import conn
from decouple import config
from models.models import mujeres
from schemas.schemas import Mujer

oauth_schema = OAuth2PasswordBearer(tokenUrl="login")

ALGORITHM = config("ALGORITHM")
SECRET_KEY = config("SECRET_KEY")

async def auth_mujer(token: str = Depends(oauth_schema)):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        documento = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("sub")
        if documento is None:
            raise exception
    except jwt.PyJWTError:
        raise exception
    return Mujer.mujer_schema(conn.execute(mujeres.select().where(mujeres.c.documento == documento)).fetchone())

async def mujer_actual(current: Mujer = Depends(auth_mujer)):
    return current