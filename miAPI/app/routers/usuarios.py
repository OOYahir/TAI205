from fastapi import status, HTTPException, Depends, APIRouter
from app.data.database import usuarios
from app.models.usuarios import crear_usuario
from app.security.auth import verificar_peticion

from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import usuario as usuarioDB

routerU=APIRouter(# usamos routeru para organizar y modularizar el codigo, para no tener todo en main.py
    prefix="/v1/usuarios",#
    tags=['CRUD HTTP']
)
#GET
@routerU.get("/") 
async def consultaT(db:Session= Depends(get_db)):
    queryUsuarios= db.query(usuarioDB).all() 
    return{
        "status":"200",
        "total": len(queryUsuarios),
        "data": queryUsuarios
    }
#POST   
@routerU.post("/", status_code=status.HTTP_201_CREATED) 
async def crea_usuario(usuarioP:crear_usuario, db:Session= Depends(get_db)):
    usuarioNuevo= usuarioDB(nombre = usuarioP.nombre, edad= usuarioP.edad)
    db.add(usuarioNuevo)
    db.commit()
    db.refresh(usuarioNuevo)
    
    return{
        "mensaje": "usuario agregado correctamente",
        "usuario":usuarioP
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
