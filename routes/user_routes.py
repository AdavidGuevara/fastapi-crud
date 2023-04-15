from fastapi import APIRouter
from config.coneccion import SessionLocal
from starlette.responses import RedirectResponse
from fastapi.params import Depends
from sqlalchemy.orm import Session
from schemas import user_schemas
from typing import List
from models.user_model import User

user = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@user.get("/")
def main():
    return RedirectResponse(url="/docs/")


@user.get("/usuarios/", response_model=List[user_schemas.User], description="Get a list of all users",)
def show_users(db: Session = Depends(get_db)):
    usuarios = db.query(User).all()
    return usuarios


@user.post("/usuarios/", response_model=user_schemas.User, description="Create a new user")
def create_users(entrada: user_schemas.User, db: Session = Depends(get_db)):
    usuario = User(
        username=entrada.username,
        nombre=entrada.nombre,
        rol=entrada.rol,
        estado=entrada.estado,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@user.put("/usuarios/{usuario_id}", response_model=user_schemas.User, description="Update a User by Id")
def update_users(
    usuario_id: int, entrada: user_schemas.UserUpdate, db: Session = Depends(get_db)
):
    usuario = db.query(User).filter_by(id=usuario_id).first()
    usuario.username = entrada.username
    usuario.rol = entrada.rol
    usuario.estado = entrada.estado
    db.commit()
    db.refresh(usuario)
    return usuario


@user.delete("/usuarios/{usuario_id}", response_model=user_schemas.Respuesta)
def delete_users(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(User).filter_by(id=usuario_id).first()
    db.delete(usuario)
    db.commit()
    respuesta = user_schemas.Respuesta(mensaje="Eliminado exitosamente")
    return respuesta
