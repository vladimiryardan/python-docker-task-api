from sqlalchemy.orm import Session

from app.models import Task
from app.schemas import TaskCreate, TaskUpdate


def get_tasks(db: Session):
    return db.query(Task).all()


def get_task_by_id(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()


def create_task(db: Session, task: TaskCreate):
    new_task = Task(
        title=task.title,
        completed=task.completed,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


def update_task(db: Session, existing_task: Task, task: TaskUpdate):
    if task.title is not None:
        existing_task.title = task.title

    if task.completed is not None:
        existing_task.completed = task.completed

    db.commit()
    db.refresh(existing_task)

    return existing_task


def delete_task(db: Session, task: Task):
    db.delete(task)
    db.commit()