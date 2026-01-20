import logging
import time
import os
from rich.logging import RichHandler
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.tree import Tree
from rich.panel import Panel

# Rich konsolunu başlat
console = Console()

class VisualLogger:
    def __init__(self):
        # 1. Rich Handler ile Renkli Loglama
        # Tarih, saat ve dosya yolunu otomatik renkli basar.
        logging.basicConfig(
            level="INFO",
            format="%(message)s",
            datefmt="[%X]",
            handlers=[RichHandler(rich_tracebacks=True, console=console)]
        )
        self.logger = logging.getLogger("rich")
    
    def get_logger(self):
        return self.logger

    def show_intro(self):
        """Program başlarken havalı bir panel gösterir."""
        console.print(Panel.fit(
            "[bold cyan]Dosya Organizasyon Scripti[/bold cyan]\n"
            "[yellow]Versiyon:[/yellow] 1.0\n"
            "[yellow]Takım:[/yellow] 7 Kişilik Dev Kadro\n"
            "[green]Hedef:[/green] Kaostan Düzene!",
            title="Başlatılıyor",
            border_style="blue"
        ))

    def show_summary_tree(self, source_folder, organized_stats):
        """
        İşlem bitince klasör yapısını ağaç şeklinde çizer.
        Grafiksel görselleştirmenin zirvesi burasıdır.
        """
        tree = Tree(f"[bold blue]{source_folder}[/bold blue]")
        
        for category, count in organized_stats.items():
            # Dalları ekle
            branch = tree.add(f"[bold green]{category}[/bold green] ({count} dosya)")
            # Altına sembolik örnekler ekleyebilirsin
            branch.add(f"[italic]...dosyalar...[/italic]")

        console.print("\n")
        console.print(Panel(tree, title="Organizasyon Sonucu", border_style="green"))

# --- SİMÜLASYON (Task 3 Entegrasyonu İçin Örnek) ---
if __name__ == "__main__":
    visual_tool = VisualLogger()
    log = visual_tool.get_logger()
    
    # 1. Intro Göster
    visual_tool.show_intro()
    
    files_to_move = ["report.pdf", "photo.jpg", "music.mp3", "notes.txt", "video.mp4"] * 4 # 20 dosya
    
    with Progress(
        SpinnerColumn(),        
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),            
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console         
    ) as progress:
        
        task1 = progress.add_task("[cyan]Dosyalar taranıyor...", total=len(files_to_move))
        
        stats = {"Documents": 0, "Images": 0, "Media": 0}
        
        for file in files_to_move:
            time.sleep(0.2) 
            
            if "pdf" in file:
                log.info(f"Taşınıyor: [bold white]{file}[/bold white] -> [blue]Documents[/blue]")
                stats["Documents"] += 1
            elif "jpg" in file:
                log.info(f"Taşınıyor: [bold white]{file}[/bold white] -> [magenta]Images[/magenta]")
                stats["Images"] += 1
            else:
                log.warning(f"Bilinmeyen tür: [bold red]{file}[/bold red] -> [yellow]Media[/yellow]")
                stats["Media"] += 1
            
            progress.update(task1, advance=1)
            
    # 3. Sonuç Ağacı
    log.info("Tüm işlemler tamamlandı! Özet hazırlanıyor...")
    visual_tool.show_summary_tree("/User/Downloads", stats)