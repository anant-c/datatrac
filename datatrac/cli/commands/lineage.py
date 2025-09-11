# datatrac/cli/commands/lineage.py
import typer
from typing import Optional
from typing_extensions import Annotated
from rich.console import Console
from rich.tree import Tree
from datatrac.core.db import get_db
from datatrac.core.manager import DataManager

app = typer.Typer(help="Create or view dataset lineage.")
console = Console()

@app.callback(invoke_without_command=True)
def lineage(
    hash_to_view: Annotated[Optional[str], typer.Argument(help="The hash of the dataset to view lineage for.")] = None,
    parent: Annotated[Optional[str], typer.Option("--parent", help="Hash of the parent dataset.")] = None,
    child: Annotated[Optional[str], typer.Option("--child", help="Hash of the child (derived) dataset.")] = None,
):
    """
    View lineage for a dataset OR create a new lineage link.

    - To VIEW: datatrac lineage <hash>
    - To CREATE: datatrac lineage --parent <hash1> --child <hash2>
    """
    db = next(get_db())
    manager = DataManager(db)

    # --- Mode 1: View Lineage ---
    if hash_to_view:
        try:
            dataset = manager.find_by_hash(hash_to_view)
            if not dataset:
                console.print(f"[red]Dataset with hash {hash_to_view} not found.[/red]")
                raise typer.Exit(1)
            
            lineage_data = manager.get_lineage(hash_to_view)

            tree = Tree(f"⛓️ [bold]Lineage for [cyan]{dataset.name}[/cyan] ([yellow]{dataset.hash[:12]}...[/yellow])")
            
            # Add parents
            if lineage_data["parents"]:
                parent_branch = tree.add("🔼 [bold green]Parents[/bold green] (Derived From)")
                for p in lineage_data["parents"]:
                    parent_branch.add(f"[cyan]{p['name']}[/cyan] ([yellow]{p['hash'][:12]}...[/yellow])")
            else:
                 tree.add("🔼 No parents found.")

            # Add children
            if lineage_data["children"]:
                child_branch = tree.add("🔽 [bold magenta]Children[/bold magenta] (Derived To)")
                for c in lineage_data["children"]:
                    child_branch.add(f"[cyan]{c['name']}[/cyan] ([yellow]{c['hash'][:12]}...[/yellow])")
            else:
                tree.add("🔽 No children found.")

            console.print(tree)

        except (FileNotFoundError, RuntimeError) as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

    # --- Mode 2: Create Lineage ---
    elif parent and child:
        try:
            manager.create_lineage(parent_hash=parent, child_hash=child)
            console.print(
                "✅ Lineage created: "
                f"[yellow]{parent[:8]}...[/yellow] -> [green]{child[:8]}...[/green]"
            )
        except ValueError as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
    
    # --- No valid options provided ---
    else:
        console.print("Usage error: Provide a hash to view, or --parent and --child to create a link.")
        raise typer.Exit(1)