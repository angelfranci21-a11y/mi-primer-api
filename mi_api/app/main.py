from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, engine
from fastapi import status
from fastapi.staticfiles import StaticFiles


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    estudiantes = db.query(models.estudiantes).all()
    return templates.TemplateResponse("index.html", {"request": request, "estudiantes": estudiantes})

@app.get("/estudiantes")
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(models.estudiantes).all()

@app.post("/estudiantes", response_model=schemas.estudiantesCreate)
def crear_estudiante(estudiantes: schemas.estudiantesCreate, db: Session = Depends(get_db)):
    existente = db.query(models.estudiantes).filter_by(carnet=estudiantes.carnet).first()
    if existente:
        raise HTTPException(status_code=400, detail="Este carnet ya existe")
    db_estudiantes = models.estudiantes(**estudiantes.dict())
    db.add(db_estudiantes)
    db.commit()
    db.refresh(db_estudiantes)
    return db_estudiantes

@app.delete("/estudiantes/{carnet}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_estudiantes(carnet: int, db: Session = Depends(get_db)):
    estudiantes = db.query(models.estudiantes).filter(models.estudiantes.carnet == carnet).first()
    if not estudiantes:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    db.delete(estudiantes)
    db.commit()
    return {"message": f"Estudiante con carnet {carnet} eliminado"}
