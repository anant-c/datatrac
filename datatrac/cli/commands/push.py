# datatrac/cli/commands/push.py
from typing import Annotated
import typer
from rich.console import Console
from datatrac.core.db import get_db
from datatrac.core.manager import DataManager

app = typer.Typer(help="Push a dataset to the registry.")
console = Console()

@app.callback(invoke_without_command=True)
def push(
    local_path: Annotated[str, typer.Argument(help="The local path to the dataset file.")],
    source: Annotated[str, typer.Option("--source", "-s", help="The original source URL of the dataset.")] = None
):
    """
    Hash a local dataset file and add it to the registry.
    """
    try:
        db_session = next(get_db())
        manager = DataManager(db_session)
        # Capture both the dataset and the new boolean flag
        dataset, was_uploaded = manager.push_dataset(local_path, source)

        # Only print the "success" message if a new upload happened
        if was_uploaded:
            console.print(f"✅ Dataset '[bold cyan]{dataset.name}[/bold cyan]' pushed successfully!")
        
        # Always print the hash
        console.print(f"   Hash: [yellow]{dataset.hash}[/yellow]")

    except FileNotFoundError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred:[/bold red] {e}")