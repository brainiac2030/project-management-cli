import uuid

class Task:
    """Represents a task within a project."""
    VALID_STATUSES = ["Pending", "In Progress", "Completed"]

    def __init__(self, title: str, status: str, assigned_to: list, project_id: str, task_id: str = None):
        self.task_id = task_id or str(uuid.uuid4())
        self.title = title
        self.status = status
        self.assigned_to = assigned_to
        self.project_id = project_id

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str):
        if value not in self.VALID_STATUSES:
            raise ValueError(f"Status must be one of {self.VALID_STATUSES}")
        self._status = value

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "title": self.title,
            "status": self.status,
            "assigned_to": self.assigned_to,
            "project_id": self.project_id
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        return cls(
            title=data["title"],
            status=data["status"],
            assigned_to=data["assigned_to"],
            project_id=data["project_id"],
            task_id=data.get("task_id")
        )
