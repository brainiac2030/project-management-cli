import uuid
from .person import Person

class User(Person):
    """Represents a system user."""
    _id_counter = 0

    def __init__(self, name: str, email: str, user_id: str = None):
        super().__init__(name, email)
        self.user_id = user_id or str(uuid.uuid4())
        User._id_counter += 1

    def to_dict(self) -> dict:
        return {"user_id": self.user_id, "name": self.name, "email": self.email}

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        return cls(name=data["name"], email=data["email"], user_id=data.get("user_id"))

    def __repr__(self) -> str:
        return f"User(id='{self.user_id}', name='{self.name}')"
