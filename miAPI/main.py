#1. Importaciones
from fastapi import FastAPI

#2. Inicializacion APP
app=FastAPI()

#3. Endpoints
@app.get("/")
async def HolaMundo():
    return {"mensaje":"Hola mundo FASTAPI"}
        #izquierda es la llave y la derecha es el valor de la llave

@app.get("/bienvenidos")
async def Bienvenidos():
    return {"mensaje":"Bienvenidos a mi API con FASTAPI"}

#python -m uvicorn main:app --reload