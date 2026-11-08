"""Task API: three endpoints, DI via Depends, validation via Pydantic."""
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status

from app.models import Priority, Task, TaskCreate
from app.repository import TaskRepository

app = FastAPI(
    title="Task API",
    version="0.1.0",
    description="Mini project #1 — ai-ml-journey, week 1",
)

_repo = TaskRepository()  # singleton lifetime


def get_repo() -> TaskRepository:
    return _repo


RepoDep = Annotated[TaskRepository, Depends(get_repo)]


@app.post("/tasks", status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(payload: TaskCreate, repo: RepoDep) -> Task:
    """Create a task. The body is validated against TaskCreate."""
    return repo.add(payload)


@app.get("/tasks", tags=["tasks"])
def list_tasks(
    repo: RepoDep,
    priority: Priority | None = None,
    done: bool | None = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> list[Task]:
    """List tasks, optionally filtered by priority and done."""
    return repo.query(priority=priority, done=done, limit=limit)


@app.get("/tasks/{task_id}", tags=["tasks"])
def get_task(task_id: int, repo: RepoDep) -> Task:
    """Fetch one task or 404."""
    task = repo.get(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )
    return task