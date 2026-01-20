import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from config_loader import load_config
from organizer import Organizer
from logger import get_logger

class OrganizationHandler(FileSystemEventHandler):
    """Dosya sistemi olaylarını dinleyen sınıf."""
    def __init__(self, logger):
        self.logger = logger
        self.organizer = Organizer()

    def on_created(self, event):
        # Klasör ise işlem yapma
        if event.is_directory:
            return
            
        self.logger.info(f"YENİ DOSYA TESPİT EDİLDİ: {event.src_path}")
        print(f"\nAlgılandı: {Path(event.src_path).name}")
        
        # Dosya kopyalaması bazen anlık bitmez, biraz bekle
        time.sleep(1)
        
        # Organizasyonu tetikle
        self.organizer.organize_file(event.src_path)

def start_watching():
    config = load_config()
    logger = get_logger()
    
    source_dir = config["source_directory"]
    
    # Kaynak klasör kontrolü
    if not Path(source_dir).exists():
        print(f"Hata: İzlenecek klasör yok -> {source_dir}")
        return

    event_handler = OrganizationHandler(logger)
    observer = Observer()
    observer.schedule(event_handler, source_dir, recursive=False)
    observer.start()

    print(f"İzleme başlatıldı (Kaynak: {source_dir})")
    print("Watcher modu aktif... Durdurmak için Ctrl+C")
    
    logger.info(f"Watcher modu başlatıldı. Kaynak: {source_dir}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nİzleme durduruldu.")
    
    observer.join()

if __name__ == "__main__":
    start_watching()