from typing import Optional
import asyncio
from app.data.database import usuarios
from fastapi import APIRouter   
routerV=APIRouter(tags=['Inicio'])

#3. Endpoints
@routerV.get("/") 
async def HolaMundo():
    return {"mensaje":"Hola mundo FASTAPI"}
        #izquierda es la llave y la derecha es el valor de la llave

@routerV.get("/v1/bienvenidos")
async def Bienvenidos():
    return {"mensaje":"Bienvenidos a mi API con FASTAPI"}

@routerV.get("/v1/promedio")
async def promedio():
    await asyncio.sleep(3)          #simulacion peticion a otra api consulra a una base de datos 
    return {
            "Calificacion":"7.5",
            "estatus":"200"
            }

@routerV.get("/v1/parametroO/{id}") 
async def consultaUno(id:int): 
    await asyncio.sleep(3) 
    return {
        "Resultado":"usuario encontrado",
        "Estatus":"200"
        }

@routerV.get("/v1/usuarios_op/")
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

