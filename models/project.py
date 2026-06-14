import uuid

class Project:
    """Represents a project owned by a user."""
    def __init__(self, title: str, description: str, due_date: str, user_id: str, project_id: str = None):
        self.project_id = project_id or str(uuid.uuid4())
        self.title = title
        self.description = description
        self.due_date = due_date
        self.user_id = user_id

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not value:
            raise ValueError("Project title cannot be empty.")
        self._title = value.strip()

    def to_dict(self) -> dict:
        return {
            "project_id": self.project_id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "user_id": self.user_id
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Project':
        return cls(
            title=data["title"],
            description=data["description"],
            due_date=data["due_date"],
            user_id=data["user_id"],
            project_id=data.get("project_id")
        )
