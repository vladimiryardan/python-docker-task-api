from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import Task
from app.schemas import TaskCreate, TaskResponse, TaskUpdate

from app.services import tasks as task_service

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.get("", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return task_service.get_tasks(db)


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return task_service.create_task(db, task)


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
):
    existing_task = task_service.get_task_by_id(db, task_id)

    if existing_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task_service.update_task(db, existing_task, task)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    existing_task = task_service.get_task_by_id(db, task_id)

    if existing_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    task_service.delete_task(db, existing_task)