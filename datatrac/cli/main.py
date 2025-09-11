# datatrac/cli/main.py
import typer
from rich.console import Console
from datatrac.core.db import create_database_tables
from .commands import fetch, push, lineage, delete

# Initialize rich console for beautiful output
console = Console()

# Create the main Typer application
app = typer.Typer(
    name="datatrac",
    help="A tool to discover, manage, and trace data files efficiently.",
    add_completion=False,
)

# Add command groups (sub-commands)
app.add_typer(fetch.app, name="fetch")
app.add_typer(push.app, name="push")
app.add_typer(lineage.app, name="lineage")
app.add_typer(delete.app, name="delete")

@app.callback()
def main():
    """
    Manage your datasets with DataTrac.
    """
    # This is a good place to ensure the database and tables are created
    create_database_tables()

if __name__ == "__main__":
    app()