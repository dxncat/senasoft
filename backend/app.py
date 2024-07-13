from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.municipios import router as MunicipioRouter
from routes.mujeres import router as AuthRouter
from routes.servicios import router as ServicioRouter
from routes.establecimientos import router as EstablecimientoRouter
from routes.agendas import router as AgendaRouter
from routes.manzanas import router as ManzanaRouter

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=["http://localhost:5173"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"]
)

app.include_router(MunicipioRouter)
app.include_router(AuthRouter)
app.include_router(ServicioRouter)
app.include_router(EstablecimientoRouter)
app.include_router(AgendaRouter)
app.include_router(ManzanaRouter)

@app.get("/")
def read_root():
    return {"Hello": "World"}