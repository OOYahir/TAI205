#1. Importaciones
from fastapi import FastAPI, status, HTTPException
from typing import Optional
import asyncio
from pydantic import BaseModel,Field


#2. Inicializacion APP
app=FastAPI(
            title="Mi primer API",
            description="Yahir Orduña O",
            version="1.0.0"
            ) #para cambiar parametros cosas de lo de docs


#base de datos ficticia 
usuarios=[
    {"id":1, "nombre":"Yahir", "edad":21},
    {"id":2, "nombre":"Diana", "edad":20},
    {"id":3, "nombre":"daniel", "edad":20},

]

class crear_usuario(BaseModel):
   
    id:int = Field(...,gt=0, description="Identificado del usuario") 
    nombre:str= Field(..., min_length=3, max_length=50, example="Juanita")
    edad:int= Field(..., ge=1, le=123, description="Edad validad entre 1 y 123")

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
    await asyncio.sleep(3)          #simulacion peticion a otra api consulra a una base de datos 
    return {
            "Calificacion":"7.5",
            "estatus":"200"
            }
@app.get("/v1/parametroO/{id}", tags=['Parametros']) 
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

#GET
@app.get("/v1/usuarios/", tags=['CRUD HTTP']) 
async def consultaT(): 
    return{
        "status":"200",
        "total": len(usuarios),
        "data": usuarios
    }
#POST   
@app.post("/v1/usuarios/", tags=['CRUD HTTP'], status_code=status.HTTP_201_CREATED) 
async def crea_usuario(usuario:crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    usuarios.append(usuario.dict())
    return{
        "mensaje": "usuario agregado correctamente",
        "usuario":usuario
    }
#PUT
@app.put("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def actualizar_usuario(id:int, usuario:dict):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index] = usuario
            return {
                "mensaje": "usuario actualizado correctamente",
                "status":"200",
                "usuario":usuario
            }
    raise HTTPException(
        status_code=400,
        detail="Usuario no encontrado"
    )
#DELETE
@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def eliminar_usuario(id:int):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            del usuarios[index]
            return {
                "mensaje": "usuario eliminado correctamente",
                "status":"200"
            }
    raise HTTPException(
        status_code=400,
        detail="Usuario no encontrado"
    )