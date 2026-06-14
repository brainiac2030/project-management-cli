import argparse
from rich.console import Console
from rich.table import Table

from models.user import User
from models.project import Project
from models.task import Task
from utils.storage import DataManager

console = Console()
db = DataManager()

# ====================== HELPER FUNCTIONS ======================
def get_user_by_name(name: str):
    for u in db.get_users():
        if u['name'].lower() == name.lower():
            return u
    return None

def get_project_by_title(title: str):
    for p in db.get_projects():
        if p['title'].lower() == title.lower():
            return p
    return None

# ====================== COMMAND HANDLERS ======================
def add_user(args):
    if get_user_by_name(args.name):
        console.print(f"[red]Error: User '{args.name}' already exists.[/red]")
        return
    try:
        new_user = User(name=args.name, email=args.email)
        users = db.get_users()
        users.append(new_user.to_dict())
        db.save_users(users)
        console.print(f"[green]✓ Successfully added user: {args.name} ({args.email})[/green]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")

def list_users(args):
    users = db.get_users()
    if not users:
        console.print("[yellow]No users found.[/yellow]")
        return
    table = Table(title="Users")
    table.add_column("Name", style="cyan")
    table.add_column("Email", style="magenta")
    for u in users:
        table.add_row(u['name'], u['email'])
    console.print(table)

def add_project(args):
    user = get_user_by_name(args.user)
    if not user:
        console.print(f"[red]Error: User '{args.user}' not found.[/red]")
        return
    if any(p['title'].lower() == args.title.lower() for p in db.get_projects()):
        console.print(f"[red]Error: Project '{args.title}' already exists.[/red]")
        return
    try:
        new_project = Project(
            title=args.title,
            description=args.description,
            due_date=args.due_date,
            user_id=user['user_id']
        )
        projects = db.get_projects()
        projects.append(new_project.to_dict())
        db.save_projects(projects)
        console.print(f"[green]✓ Successfully added project '{args.title}' to '{args.user}'.[/green]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")

def list_projects(args):
    projects = db.get_projects()
    users = db.get_users()
    user_map = {u['user_id']: u['name'] for u in users}

    if args.user:
        target_user = get_user_by_name(args.user)
        if not target_user:
            console.print(f"[red]Error: User '{args.user}' not found.[/red]")
            return
        projects = [p for p in projects if p['user_id'] == target_user['user_id']]

    if not projects:
        console.print("[yellow]No projects found.[/yellow]")
        return

    table = Table(title="Projects")
    table.add_column("Title", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Due Date", style="yellow")
    table.add_column("Owner", style="magenta")
    for p in projects:
        table.add_row(p['title'], p['description'], p['due_date'], user_map.get(p['user_id'], 'Unknown'))
    console.print(table)

def add_task(args):
    project = get_project_by_title(args.project)
    if not project:
        console.print(f"[red]Error: Project '{args.project}' not found.[/red]")
        return

    assigned_names = [name.strip() for name in args.assigned_to.split(',')]
    assigned_ids = []
    for name in assigned_names:
        user = get_user_by_name(name)
        if not user:
            console.print(f"[yellow]Warning: User '{name}' not found. Skipping.[/yellow]")
        else:
            assigned_ids.append(user['user_id'])

    if not assigned_ids:
        console.print("[red]Error: No valid users assigned to the task.[/red]")
        return

    try:
        new_task = Task(
            title=args.title,
            status=args.status,
            assigned_to=assigned_ids,
            project_id=project['project_id']
        )
        tasks = db.get_tasks()
        tasks.append(new_task.to_dict())
        db.save_tasks(tasks)
        console.print(f"[green]✓ Successfully added task '{args.title}' to project '{args.project}'.[/green]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")

def list_tasks(args):
    project = get_project_by_title(args.project)
    if not project:
        console.print(f"[red]Error: Project '{args.project}' not found.[/red]")
        return

    tasks = [t for t in db.get_tasks() if t['project_id'] == project['project_id']]
    users = db.get_users()
    user_map = {u['user_id']: u['name'] for u in users}

    if not tasks:
        console.print("[yellow]No tasks found for this project.[/yellow]")
        return

    table = Table(title=f"Tasks for Project: {args.project}")
    table.add_column("Title", style="cyan")
    table.add_column("Status", style="yellow")
    table.add_column("Assigned To", style="magenta")
    for t in tasks:
        assignees = [user_map.get(uid, 'Unknown') for uid in t['assigned_to']]
        table.add_row(t['title'], t['status'], ", ".join(assignees))
    console.print(table)

def complete_task(args):
    project = get_project_by_title(args.project)
    if not project:
        console.print(f"[red]Error: Project '{args.project}' not found.[/red]")
        return

    tasks = db.get_tasks()
    task_found = False
    for t in tasks:
        if t['project_id'] == project['project_id'] and t['title'].lower() == args.task.lower():
            t['status'] = "Completed"
            task_found = True
            break

    if task_found:
        db.save_tasks(tasks)
        console.print(f"[green]✓ Successfully marked task '{args.task}' as Completed.[/green]")
    else:
        console.print(f"[red]Error: Task '{args.task}' not found in project '{args.project}'.[/red]")

# ====================== CLI SETUP ======================
def main():
    parser = argparse.ArgumentParser(description="Project Management CLI Tool", prog="python main.py")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # add user
    p_add_user = subparsers.add_parser("add-user", help="Add a new user")
    p_add_user.add_argument("--name", required=True, help="User's name")
    p_add_user.add_argument("--email", required=True, help="User's email")

    # list users
    subparsers.add_parser("list-users", help="List all users")

    # add project
    p_add_proj = subparsers.add_parser("add-project", help="Add a new project")
    p_add_proj.add_argument("--user", required=True, help="Owner's name")
    p_add_proj.add_argument("--title", required=True, help="Project title")
    p_add_proj.add_argument("--description", default="No description", help="Project description")
    p_add_proj.add_argument("--due_date", default="TBD", help="Due date (YYYY-MM-DD)")

    # list projects
    p_list_proj = subparsers.add_parser("list-projects", help="List projects")
    p_list_proj.add_argument("--user", help="Filter by user name")

    # add task
    p_add_task = subparsers.add_parser("add-task", help="Add a new task")
    p_add_task.add_argument("--project", required=True, help="Project title")
    p_add_task.add_argument("--title", required=True, help="Task title")
    p_add_task.add_argument("--status", default="Pending", choices=["Pending", "In Progress", "Completed"])
    p_add_task.add_argument("--assigned_to", required=True, help="Comma-separated user names")

    # list tasks
    p_list_tasks = subparsers.add_parser("list-tasks", help="List tasks for a project")
    p_list_tasks.add_argument("--project", required=True, help="Project title")

    # complete task
    p_complete = subparsers.add_parser("complete-task", help="Mark a task as completed")
    p_complete.add_argument("--project", required=True, help="Project title")
    p_complete.add_argument("--task", required=True, help="Task title")

    args = parser.parse_args()

    commands = {
        "add-user": add_user,
        "list-users": list_users,
        "add-project": add_project,
        "list-projects": list_projects,
        "add-task": add_task,
        "list-tasks": list_tasks,
        "complete-task": complete_task,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
