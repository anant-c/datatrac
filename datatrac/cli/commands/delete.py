# datatrac/cli/commands/delete.py
import typer
from typing import Optional
from typing_extensions import Annotated
from rich.console import Console
from datatrac.core.db import get_db
from datatrac.core.manager import DataManager

ADMIN_PASSWORD = "admin"
app = typer.Typer(help="Delete a dataset remotely (admin) or locally.")
console = Console()

@app.callback(invoke_without_command=True)
def delete(
    hash_to_delete: Annotated[str, typer.Argument(help="Full hash of the dataset to delete.")],
    local: Annotated[bool, typer.Option("--local", "-l", help="Delete the dataset from the local machine only.")] = False,
    password: Annotated[Optional[str], typer.Option(help="Admin password for remote deletion.")] = None,
):
    db = next(get_db())
    manager = DataManager(db)

    if local:
        success, message = manager.delete_local_copy(hash_to_delete)
        if success:
            console.print(f"✅ {message}")
        else:
            console.print(f"[bold red]Error:[/bold red] {message}")
        return

    # --- Remote Delete Logic ---
    if not password:
        password = typer.prompt("Admin password required for remote delete", hide_input=True)

    if password != ADMIN_PASSWORD:
        console.print("[bold red]Error: Invalid admin password.[/bold red]")
        raise typer.Exit(code=1)
    
    success, message = manager.delete_dataset(hash_to_delete)
    if success:
        console.print(f"✅ {message}")
    else:
        console.print(f"[bold red]Error:[/bold red] {message}")