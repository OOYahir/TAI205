#1. Importaciones
from fastapi import FastAPI, status, HTTPException, Depends
from typing import Optional
import asyncio
from pydantic import BaseModel,Field
#from fastapi.security import HTTPBasic, HTTPBasicCredentials
#import secrets
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from datetime import datetime, timedelta

#2. Inicializacion APP
app=FastAPI(
            title="Mi primer API",
            description="Yahir Orduña O",
            version="1.0.0"
            ) #para cambiar parametros cosas de lo de docs

#config del token
secret_key="clavesecreta"
algoritmo="HS256"
acceso_token_expiracion=30

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="token")

usuarios_login={
    "yahir":"1234"
}

def crear_token(data: dict):
    datos=data.copy()
    expiracion=datetime.utcnow() + timedelta(minutes=acceso_token_expiracion)
    datos.update({"exp": expiracion})
    token=jwt.encode(datos, secret_key, algorithm=algoritmo)
    return token

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

#4. Seguridad HTTP Basic
# seguridad= HTTPBasic()
# def verificar_peticion(credenciales: HTTPBasicCredentials=Depends(seguridad)):
#     userAuth= secrets.compare_digest(credenciales.username,"ivanisay")
#     #userAuth= secrets.compare_digest(intento, validas)
#     passAuth= secrets.compare_digest(credenciales.password,"123456")
#     if not (userAuth and passAuth):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Credenciales no autorizadas"
#         )
#     return credenciales.username

@app.post("/token", tags=["Seguridad"])
async def login(form_data:OAuth2PasswordRequestForm=Depends()):
    password=usuarios_login.get(form_data.username)
    if password is None or password!=form_data.password:
        raise HTTPException(
            status_code=401,
            detail="credenciales incorrectas"
        )
    token=crear_token({"sub":form_data.username})
    return{
        "access_token":token,
        "token_type":"bearer"
    }
async def validar_token(token:str=Depends(oauth2_scheme)):

    try:

        datos=jwt.decode(token,secret_key,algorithms=[algoritmo])

        usuario=datos.get("sub")

        if usuario is None:
            raise HTTPException(status_code=401,detail="token invalido")

        return usuario

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="token invalido o expirado"
        )

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
async def actualizar_usuario(id:int, usuario:dict, user:str=Depends(validar_token)):
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
#async def eliminar_usuario(id:int,userAuth:str=Depends(verificar_peticion)):
async def eliminar_usuario(id:int, user:str=Depends(validar_token)):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios.pop(index)
            #del usuarios[index]
            return {
                "mensaje": f"usuario eliminado correctamente",
                "status":"200"
            }
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )
