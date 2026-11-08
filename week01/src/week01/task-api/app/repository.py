"""In-memory task storage. Swap for a database later without touching routes."""
from datetime import datetime, timezone
from threading import Lock

from app.models import Priority, Task, TaskCreate


class TaskRepository:
    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id = 1
        self._lock = Lock()  # def-handlers run on a thread pool, so guard writes

    def add(self, data: TaskCreate) -> Task:
        with self._lock:
            task = Task(
                id=self._next_id,
                created_at=datetime.now(timezone.utc),
                **data.model_dump(),
            )
            self._tasks[task.id] = task
            self._next_id += 1
        return task

    def get(self, task_id: int) -> Task | None:
        return self._tasks.get(task_id)

    def query(
        self,
        priority: Priority | None = None,
        done: bool | None = None,
        limit: int = 20,
    ) -> list[Task]:
        items = self._tasks.values()
        if priority is not None:
            items = [t for t in items if t.priority == priority]
        if done is not None:
            items = [t for t in items if t.done == done]
        return list(items)[:limit]