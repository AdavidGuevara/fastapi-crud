from sqlalchemy import Column, Integer, String
from config.coneccion import Base, engine


class User(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    nombre = Column(String(50))
    rol = Column(String(200))
    estado = Column(Integer)


Base.metadata.create_all(bind=engine)
