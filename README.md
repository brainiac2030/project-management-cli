# Project Management CLI Tool

A Python based CommandLine Interface application for managing users, projects, and tasks with local JSON persistence.

## Setup Instructions
1. Clone the repository:
2. Navigate to the directory: `cd project_manager`
3. Install dependencies: `pip install -r requirements.txt`

## CLI Commands
- **Add User**: `python main.py add-user --name "Alex" --email "alex@example.com"`
- **List Users**: `python main.py list-users`
- **Add Project**: `python main.py add-project --user "Alex" --title "CLI Tool" --description "Build a CLI" --due_date "2026-12-31"`
- **List Projects**: `python main.py list-projects` (or `--user "Alex"` to filter)
- **Add Task**: `python main.py add-task --project "CLI Tool" --title "Implement add-task" --status "Pending" --assigned_to "Alex"`
- **List Tasks**: `python main.py list-tasks --project "CLI Tool"`
- **Complete Task**: `python main.py complete-task --project "CLI Tool" --task "Implement add-task"`

## Architecture
- **`models/`**: OOP classes with encapsulation and serialization.
- **`utils/`**: `DataManager` handles robust JSON I/O with `try-except` error handling.
- **`main.py`**: Modular `argparse` CLI routing with `rich` for formatted terminal output.

##  Testing
Run the test suite using pytest
```bash
pytest tests/ -v