import typer
from rich.console import Console
from rich.text import Text

console = Console()

def app_main(name: str = typer.Argument(default="world")):
    text = Text(f"Hello {name}!", style="bold green on black")
    console.print(text)

def main():
    typer.run(app_main)

if __name__ == "__main__":
    main()
