from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.post("/workers/", response_model=schemas.Worker)
def create_worker(worker: schemas.WorkerBase, db: Session = Depends(get_db)):
    db_user = crud.get_worker_by_name(db, name=worker.name)
    if db_user:
        raise HTTPException(status_code=400, detail="Name already exists")
    return crud.create_worker(db=db, worker=worker)


@app.get("/workers/", response_model=List[schemas.Worker])
def get_workers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    workers = crud.get_workers(db, skip=skip, limit=limit)
    return workers


@app.get("/workers/{worker_id}", response_model=schemas.Worker)
def get_worker(worker_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_worker(db, worker_id=worker_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return db_user


@app.delete("/workers/{worker_id}")
def delete_worker(worker_id: int, db: Session = Depends(get_db)):
    return crud.delete_worker(db=db, worker_id=worker_id)


@app.post("/workers/{worker_id}/teams/", response_model=schemas.Team)
def create_team_for_user(
    worker_id: int, team: schemas.TeamCreate, db: Session = Depends(get_db)
):
    return crud.create_user_team(db=db, team=team, worker_id=worker_id)


@app.get("/teams/", response_model=List[schemas.Team])
def read_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    teams = crud.get_teams(db, skip=skip, limit=limit)
    return teams
