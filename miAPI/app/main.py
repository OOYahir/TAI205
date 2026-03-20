#1. Importaciones
from fastapi import FastAPI
from app.routers import usuarios, varios


#2. Inicializacion APP
app=FastAPI(
            title="Mi primer API",
            description="Yahir Orduña O",
            version="1.0.0"
            ) #para cambiar parametros cosas de lo de docs
app.include_router(usuarios.routerU)#usamos para que se inicialice con la app
app.include_router(varios.routerV)