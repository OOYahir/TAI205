#1. Importaciones
from fastapi import FastAPI
from app.routers import usuarios, varios

from app.data.db import engine
from app.data import usuario
usuario.Base.metadata.create_all(bind=engine) 


#2. Inicializacion APP
app=FastAPI(
            title="Mi primer API",
            description="Yahir Orduña O",
            version="1.0.0"
            ) #para cambiar parametros cosas de lo de docs
app.include_router(usuarios.routerU)#usamos para que se inicialice con la app
app.include_router(varios.routerV)