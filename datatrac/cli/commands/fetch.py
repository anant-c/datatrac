# datatrac/cli/commands/fetch.py
from typing import Annotated, Optional
import typer
from rich.console import Console
from rich.table import Table
from datatrac.core.db import get_db
from datatrac.core.manager import DataManager, get_current_user

app = typer.Typer(help="Fetch dataset information from the registry.")
console = Console()

@app.callback(invoke_without_command=True)
def fetch(
    hash_prefix: Annotated[Optional[str], typer.Argument(help="The full hash of the dataset.")] = None,
    list_all: Annotated[bool, typer.Option("--all", "-a", help="List all datasets in the registry.")] = False,
    download: Annotated[bool, typer.Option("--download", help="Download the specified dataset.")] = False,
):
    db = next(get_db())
    manager = DataManager(db)

    if download:
        if not hash_prefix:
            console.print("[bold red]Error:[/bold red] You must provide a dataset hash to download.")
            raise typer.Exit(code=1)
        try:
            path, message = manager.download_dataset(hash_prefix)
            console.print(f"✅ {message}")
            if path:
                console.print(f"   Path: [green]{path}[/green]")
        except (FileNotFoundError, RuntimeError) as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
        return

    if list_all:
        datasets = manager.find_all()
        if not datasets:
            console.print("No datasets found in the registry.")
            return
        
        console.print(f"Viewing as user: [bold yellow]{get_current_user()}[/bold yellow]")
        table = Table("Name", "Hash", "Your Local Path", "Created At")
        for ds in datasets:
            local_path = manager.find_local_path_for_user(ds.hash)
            local_path_display = str(local_path) if local_path else "N/A (Remote)"
            table.add_row(ds.name, ds.hash, local_path_display, str(ds.created_at))
        console.print(table)
        
    elif hash_prefix:
        dataset = manager.find_by_hash(hash_prefix)
        if not dataset:
            console.print(f"[bold red]Error:[/bold red] Dataset with hash '{hash_prefix}' not found.")
            return
            
        console.print(f"[bold]Dataset Details for {dataset.name}[/bold]")
        console.print(f"  [cyan]Full Hash:[/cyan] {dataset.hash}")
        console.print(f"  [cyan]Source:[/cyan] {dataset.source or 'N/A'}")
        console.print(f"  [cyan]Original Path:[/cyan] {dataset.local_path}")
        console.print(f"  [cyan]Registry Path:[/cyan] {dataset.registry_path}")
        console.print(f"  [cyan]Created At:[/cyan] {dataset.created_at}")
    else:
        console.print("Please specify a dataset hash or use the --all or --download flag.")