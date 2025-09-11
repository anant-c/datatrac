# datatrac/cli/commands/delete.py
import typer
from typing_extensions import Annotated
from rich.console import Console
from datatrac.core.db import get_db
from datatrac.core.manager import DataManager

# In a real app, this would come from a secure config file or env variable
ADMIN_PASSWORD = "admin"

app = typer.Typer(help="Delete a dataset from the registry.")
console = Console()

@app.callback(invoke_without_command=True)
def delete(
    hash_to_delete: Annotated[str, typer.Argument(help="Full hash of the dataset to delete.")],
    password: Annotated[str, typer.Option(
        "--password",
        prompt=True,
        hide_input=True,
        help="Admin password is required to delete."
    )]
):
    """
    Permanently delete a dataset from the registry and filesystem.
    """
    if password != ADMIN_PASSWORD:
        console.print("[bold red]Error: Invalid admin password.[/bold red]")
        raise typer.Exit(code=1)

    try:
        db = next(get_db())
        manager = DataManager(db)
        success = manager.delete_dataset(hash_to_delete)
        if success:
            console.print(f"✅ Dataset [yellow]{hash_to_delete[:12]}...[/yellow] has been deleted.")
        else:
            console.print(f"[bold red]Error:[/bold red] Dataset with hash '{hash_to_delete}' not found.")
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred:[/bold red] {e}")