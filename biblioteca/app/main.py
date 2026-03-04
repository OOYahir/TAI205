
from fastapi import FastAPI, status, HTTPException
from typing import Optional
import asyncio
from pydantic import BaseModel,Field

app=FastAPI(
            title="Biblioteca",
            description="Yahir Orduña O",
            version="1.0.0"
            ) 
class  usuario(BaseModel):
    id:int
    nombre:str
    correo:str

class Libro(BaseModel):
    id:int
    nombre:str = Field(..., min_length=2, max_length=100, example="La cronica de una muerte anunciada")
    autor:str = Field(..., min_length=2, max_length=50, example="gabriel garcia")
    estado:str = "disponible"
    año:int = Field(..., gt=1450, le=2026, description="año valido entre 1450 y 2026")
    paginas:int = Field(..., gt=1, description="numero de paginas debe ser mayor a 1")

class Prestamo(BaseModel):
    nombre_libro: str = Field(..., min_length=2, max_length=100, example="La cronica de una muerte anunciada")
    usuario: usuario 

#base
libros=[{"id":1, "nombre":"La cronica de una muerte anunciada", "autor":"gabriel garcia", "estado":"disponible", "año":1981, "paginas":200},]
prestamos=[{"nombre_libro":"La cronica de una muerte anunciada", "usuario":{"id":1, "nombre":"Yahir", "correo":"yahir@gmail.com"}}]

#registra un libro
@app.post("/v1/libros/", tags=["CRUD biblioteca"], status_code=status.HTTP_201_CREATED)
async def crear_libro(libro: Libro):

    for l in libros:
        if l["id"] == libro.id:
            raise HTTPException(
                status_code=400,
                detail="Ya existe un libro con ese ID"
            )

    libros.append(libro.dict())

    return {
        "mensaje": "Libro registrado correctamente",
        "libro": libro
    }
#lista de libros disponibles
@app.get("/v1/libros/", tags=["CRUD biblioteca"])
async def consulta_libros():

    disponibles = []

    for libro in libros:
        if libro["estado"] == "disponible":
            disponibles.append(libro)

    return {
        "total": len(disponibles),
        "data": disponibles
    }
#buscar un libro por nombre
@app.get("/v1/libros/{nombre}", tags=["CRUD biblioteca"])
async def buscar_libro(nombre: str):

    for libro in libros:
        if libro["nombre"].lower() == nombre.lower():
            return libro

    raise HTTPException(
        status_code=404,
        detail="Libro no encontrado"
    )
#registrar un préstamo
@app.post("/v1/libros/prestamos/", tags=["CRUD biblioteca"])
async def registrar_prestamo(prestamo: Prestamo):

    for libro in libros:

        if libro["nombre"].lower() == prestamo.nombre_libro.lower():

            if libro["estado"] == "prestado":
                raise HTTPException(
                    status_code=409,
                    detail="El libro ya está prestado"
                )
            libro["estado"] = "prestado"
            prestamos.append(prestamo.dict())

            return {
                "mensaje": "Préstamo registrado correctamente"
            }

    raise HTTPException(
        status_code=404,
        detail="Libro no encontrado"
    )
#marcar un libro como devuelto
@app.put("/v1/libros/prestamos/devolver/{nombre}", tags=["CRUD biblioteca"])
async def devolver_libro(nombre: str):

    for libro in libros:

        if libro["nombre"].lower() == nombre.lower():

            if libro["estado"] == "disponible":
                raise HTTPException(
                    status_code=409,
                    detail="El libro ya estaba disponible"
                )

            libro["estado"] = "disponible"

            return {
                "mensaje": "Libro devuelto correctamente"
            }

    raise HTTPException(
        status_code=404,
        detail="Libro no encontrado"
    )
#eliminar un prestamo
@app.delete("/v1/libros/prestamos/{nombre}", tags=["CRUD biblioteca"])
async def eliminar_prestamo(nombre: str):

    for prestamo in prestamos:

        if prestamo["nombre_libro"].lower() == nombre.lower():

            prestamos.remove(prestamo)

            return {
                "mensaje": "Préstamo eliminado correctamente"
            }

    raise HTTPException(
        status_code=409,
        detail="El registro de préstamo no existe"
    )
