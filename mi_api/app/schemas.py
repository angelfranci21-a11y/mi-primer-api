from pydantic import BaseModel

class estudiantesBase(BaseModel):
    carnet: int
    nombre: str
    grado: str
    edad: int

class estudiantesCreate(estudiantesBase):
    pass

class estudiantes(estudiantesBase):
    class Config:
        orm_mode = True
