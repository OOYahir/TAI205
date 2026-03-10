
from fastapi import FastAPI, status, HTTPException, Depends
from datetime import date
from pydantic import BaseModel, Field, model_validator
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets


app=FastAPI(
            title="Examen2do",
            description="Yahir Orduña O",
            version="1.0.0"
            )

class huesped(BaseModel): 
    id: int
    huesped: str = Field(...,  min_length=1, max_length=5)
    fecha_entrada: date
    fecha_salida: date
    tipo_habitacion: str = Field(...,  min_length=1, max_length=10, description="sencilla, doble o suite")
    estancia: int = Field(..., le=7, description="La estancia no puede ser mayor a 7 días")

    @model_validator(mode="after")
    def validar_fechas(self):
        if self.fecha_salida <= self.fecha_entrada:
            raise ValueError("fecha_salida debe ser mayor a fecha_entrada")
        return self
# bases
reservas=[]

#seguirdad
seguridad= HTTPBasic()
def verificar_peticion(credenciales: HTTPBasicCredentials=Depends(seguridad)):
    userAuth= secrets.compare_digest(credenciales.username,"hotel")
    passAuth= secrets.compare_digest(credenciales.password,"r2026")
    if not (userAuth and passAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no autorizadas"
        )
    return credenciales.username

#lista de reservas
@app.get("/v1/reservas/", tags=["crud"]) 
async def listar(userAuth:str=Depends(verificar_peticion)): 
    return{
        "status":"200",
        "total": len(reservas),
        "data": reservas
    }
#consultar por id
@app.get("/v1/reservas/{id}", tags=["crud"])
async def buscar_reserva(id: int):

    for reserva in reservas:
        if reserva["id"] == id:
            return reserva

    raise HTTPException(
        status_code=404,
        detail="Reserva no encontrada"
    )
#crear reserva
@app.post("/v1/reservas/", tags=["crud"], status_code=status.HTTP_201_CREATED) 
async def crear_reserva(reserva:huesped):
    for usr in reservas:
        if usr["id"] == reserva.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    reservas.append(reserva.dict())
    return{
        "mensaje": "reserva registrada correctamente",
        "reserva":reserva
    }
#confirmar reserva
@app.put("/v1/reservas/confirmar/{id}", tags=["crud"])
async def confirmar_reserva(id: int):
    for reserva in reservas:
        if reserva["id"] == id:
            reserva["confirmada"] = True
            return {
                "mensaje": "Reserva confirmada correctamente"
            }
    raise HTTPException(
        status_code=404,
        detail="Reserva no encontrada"
    )
#cancelar reserva
@app.delete("/v1/reservas/cancelar/{id}", tags=["crud"])
async def cancelar_reserva(id: int,userAuth:str=Depends(verificar_peticion)):

    for reserva in reservas:

        if reserva["id"] == id:

            reservas.remove(reserva)

            return {
                "mensaje": "Reserva cancelada"
            }

    raise HTTPException(
        status_code=409,
        detail="La reserva no existe"
    )