from sqlalchemy.orm import Session
from models.project_model import Project

def create_project(db: Session, payload):
    project = Project(**payload.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

def get_project(db: Session, project_id: int):
    return (db.query(Project).filter(Project.id == project_id).first())

def get_projects(db: Session):
    return db.query(Project).all()

def update_project(db: Session, project_id: int, payload):
    project = get_project(db, project_id)
    if not project:
        return None

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(project, key, value)
    db.commit()
    db.refresh(project)
    return project

def delete_project(db: Session, project_id: int):
    project = get_project(db, project_id)
    if not project:
        return False
    db.delete(project)
    db.commit()
    return True