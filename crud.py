from sqlalchemy.orm import Session

import models
import schemas


def get_worker(db: Session, worker_id: int):
    return db.query(models.Worker).filter(models.Worker.id == worker_id).first()


def delete_worker(db: Session, worker_id: int):
    db_user = (db.query(models.Worker).filter(
        models.Worker.id == worker_id).first())
    db.delete(db_user)
    db.commit()
    return db_user


def get_worker_by_name(db: Session, name: str):
    return db.query(models.Worker).filter(models.Worker.name == name).first()


def get_workers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Worker).offset(skip).limit(limit).all()


def create_worker(db: Session, worker: schemas.WorkerBase):
    db_user = models.Worker(name=worker.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_teams(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Team).offset(skip).limit(limit).all()


def delete_team(db: Session, team_id: int):
    db_team = (db.query(models.Team).filter(models.Team.id == team_id).first())
    db.delete(db_team)
    db.commit()
    return db_team


def create_user_team(db: Session, team: schemas.TeamCreate, worker_id: int):
    db_team = models.Team(**team.dict(), owner_id=worker_id)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team
