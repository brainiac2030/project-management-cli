import json
import os

class DataManager:
    """Handles all JSON file I/O operations."""
    def __init__(self):
        self.data_dir = "data"
        self.users_file = os.path.join(self.data_dir, "users.json")
        self.projects_file = os.path.join(self.data_dir, "projects.json")
        self.tasks_file = os.path.join(self.data_dir, "tasks.json")
        self._ensure_dir()

    def _ensure_dir(self):
        os.makedirs(self.data_dir, exist_ok=True)

    def _load(self, filename: str) -> list:
        if not os.path.exists(filename):
            return []
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def _save(self, filename: str, data: list):
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"Error saving to {filename}: {e}")

    def get_users(self) -> list:
        return self._load(self.users_file)

    def save_users(self, users: list):
        self._save(self.users_file, users)

    def get_projects(self) -> list:
        return self._load(self.projects_file)

    def save_projects(self, projects: list):
        self._save(self.projects_file, projects)

    def get_tasks(self) -> list:
        return self._load(self.tasks_file)

    def save_tasks(self, tasks: list):
        self._save(self.tasks_file, tasks)
