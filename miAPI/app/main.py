#1. Importaciones
from fastapi import FastAPI
from typing import Optional
import asyncio

#2. Inicializacion APP
app=FastAPI(
            title="Mi primer API",
            description="Yahir Orduña O",
            version="1.0.0"
            ) #para cambiar parametros cosas de lo de docs


#base de datos ficticia 
usuarios=[
    {"id":"1", "nombre":"Yahir", "edad":"21"},
    {"id":"2", "nombre":"Diana", "edad":"20"},
    {"id":"3", "nombre":"daniel", "edad":"20"},

]

#3. Endpoints
@app.get("/", tags=['Inicio']) 
async def HolaMundo():
    return {"mensaje":"Hola mundo FASTAPI"}
        #izquierda es la llave y la derecha es el valor de la llave

@app.get("/v1/bienvenidos", tags=['Inicio'])
async def Bienvenidos():
    return {"mensaje":"Bienvenidos a mi API con FASTAPI"}

@app.get("/v1/promedio", tags=['Calificaciones'])
async def promedio():
    await asyncio.sleep(3)          #simulacion peticon a otra api consulra a una base de datos 
    return {
            "Calificacion":"7.5",
            "estatus":"200"
            }
@app.get("/v1/usuario/{id}", tags=['Parametros']) 
async def consultaUno(id:int): 
    await asyncio.sleep(3) 
    return {
        "Resultado":"usuario encontrado",
        "Estatus":"200"
        }

@app.get("/v1/usuarios_op/", tags=['Parametro opcional'])
async def consultaOp(id:Optional[int]=None): 
    await asyncio.sleep(2) 
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"Usuario encontrado":id, "Datos":usuario}
            return {"Mensaje":"usuario no encontrado"}
        else:
            return {"Aviso":"no se proporciono id"}

#python -m uvicorn main:app --reload 