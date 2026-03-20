from fastapi import status, HTTPException, Depends, APIRouter
from app.data.database import usuarios
from app.models.usuarios import crear_usuario
from app.security.auth import verificar_peticion

routerU=APIRouter(# usamos routeru para organizar y modularizar el codigo, para no tener todo en main.py
    prefix="/v1/usuarios",#
    tags=['CRUD HTTP']
)
#GET
@routerU.get("/") 
async def consultaT(): 
    return{
        "status":"200",
        "total": len(usuarios),
        "data": usuarios
    }
#POST   
@routerU.post("/", status_code=status.HTTP_201_CREATED) 
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
@routerU.put("/{id}", status_code=status.HTTP_200_OK)
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
@routerU.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_usuario(id:int,userAuth:str=Depends(verificar_peticion)):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios.pop(index)
            #del usuarios[index]
            return {
                "mensaje": f"usuario eliminado por {userAuth}",
                "status":"200"
            }
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )
