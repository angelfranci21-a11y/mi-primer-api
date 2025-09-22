from sqlalchemy import Column, Integer, String
from .database import Base

class estudiantes(Base):
    __tablename__ = "estudiantes"
    __table_args__ = {"extend_existing": True}
    carnet = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    grado = Column(String)
    edad = Column(Integer)
