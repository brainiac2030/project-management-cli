import pytest
import os
import shutil
from models.user import User
from models.project import Project
from models.task import Task
from utils.storage import DataManager

@pytest.fixture
def db():
    # Use test directory
    test_dir = "test_data"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    db = DataManager()
    db.data_dir = test_dir
    db.users_file = os.path.join(test_dir, "users.json")
    db.projects_file = os.path.join(test_dir, "projects.json")
    db.tasks_file = os.path.join(test_dir, "tasks.json")
    db._ensure_dir()
    yield db
    # Cleanup
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

def test_user_creation_and_validation(db):
    user = User(name="Alex", email="alex@example.com")
    assert user.name == "Alex"
    assert user.email == "alex@example.com"
    assert user.user_id is not None

def test_invalid_email():
    with pytest.raises(ValueError):
        User(name="Alex", email="invalid-email")

def test_task_status_validation():
    task = Task(title="Test", status="Pending", assigned_to=["u1"], project_id="p1")
    assert task.status == "Pending"
    with pytest.raises(ValueError):
        task.status = "Invalid"

def test_data_persistence(db):
    user = User(name="Alex", email="alex@example.com")
    db.save_users([user.to_dict()])
    loaded = db.get_users()
    assert len(loaded) == 1
    assert loaded[0]['name'] == "Alex"
