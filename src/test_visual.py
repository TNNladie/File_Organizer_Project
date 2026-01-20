# Dosya: src/test_visual.py
import time
import random
import logging
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn
from rich.tree import Tree
from rich.panel import Panel

# --- GÖRSEL LOGGER SINIFI ---
class VisualLogger:
    def __init__(self):
        self.console = Console()
        logging.basicConfig(
            level="NOTSET",
            format="%(message)s",
            datefmt="[%X]",
            handlers=[RichHandler(rich_tracebacks=True, console=self.console, markup=True)]
        )
        self.log = logging.getLogger("rich")

    def show_intro(self):
        self.console.print(Panel.fit(
            "[bold cyan]OTOMATİK DOSYA ORGANİZATÖRÜ[/bold cyan]\n"
            "[yellow]Mod:[/yellow] Canlı İzleme\n"
            "[yellow]Durum:[/yellow] Hazır",
            title="YOLCU PROJECT",
            border_style="blue"
        ))
        time.sleep(1)

    def show_summary(self, stats):
        self.console.print("\n")
        tree = Tree("[bold blue]Downloads Klasörü (Son Durum)[/bold blue]")
        for k, v in stats.items():
            branch = tree.add(f"[bold yellow]{k}[/bold yellow] ({v} Dosya)")
            branch.add(f"[italic green]✔ Organize edildi[/italic green]")
        self.console.print(Panel(tree, title="İşlem Raporu", border_style="green"))

# --- TEST ---
if __name__ == "__main__":
    tool = VisualLogger()
    tool.show_intro()
    
    files = [f"dokuman_{i}.pdf" for i in range(1, 10)] + [f"foto_{i}.jpg" for i in range(1, 15)]
    random.shuffle(files)
    stats = {"Documents": 0, "Images": 0}

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=tool.console
    ) as progress:
        task = progress.add_task("Dosyalar Taranıyor...", total=len(files))
        for file in files:
            time.sleep(0.1)
            if "pdf" in file:
                tool.log.info(f"Taşınıyor: {file} -> Documents")
                stats["Documents"] += 1
            else:
                tool.log.info(f"Taşınıyor: {file} -> Images")
                stats["Images"] += 1
            progress.update(task, advance=1)

    tool.show_summary(stats)