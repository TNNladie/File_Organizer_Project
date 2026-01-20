import time
import logging
import os
import json
import sys
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Modül bağımlılıklarını yönet
try:
    from src.organizer import FileOrganizer
    HAS_ORGANIZER = True
except ImportError:
    # Bağımsız çalışma durumunda modül yolunu ekle
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    try:
        from src.organizer import FileOrganizer
        HAS_ORGANIZER = True
    except ImportError:
        HAS_ORGANIZER = False

class WatcherHandler(FileSystemEventHandler):
    """Dosya sistemi olaylarını işleyen sınıf."""
    def __init__(self, organizer=None):
        self.organizer = organizer

    def on_created(self, event):
        """Dosya veya klasör oluşturulduğunda tetiklenir."""
        path_type = "KLASÖR" if event.is_directory else "DOSYA"
        src_path_str = str(event.src_path)
        
        message = f"!!! YENİ {path_type} TESPİT EDİLDİ: {src_path_str} !!!"
        print(message)
        logging.info(message)
        
        # Dosya yazma işleminin tamamlanması için bekle
        time.sleep(1)
        
        # Dosya ise organize et
        if not event.is_directory and self.organizer:
            try:
                self.organizer.organize_file(src_path_str)
                print(f"-> Düzenlendi: {src_path_str}")
            except Exception as e:
                print(f"-> Düzenleme hatası: {e}")
        elif event.is_directory:
             print(f"-> Klasör tespit edildi, işlem yapılmıyor.")
        elif not self.organizer:
            print("-> Düzenleyici aktif değil, sadece izleme yapılıyor.")

class Watcher:
    """Belirtilen dizini izleyen ve değişiklikleri yöneten ana sınıf."""
    def __init__(self, directory, organizer=None):
        self.directory = str(Path(directory).resolve())
        self.organizer = organizer
        self.observer = Observer()
        self.handler = WatcherHandler(organizer)

    def start(self):
        """İzleme işlemini başlatır."""
        print(f"--- İzleyici Başlatıldı: {self.directory} ---")
        print("Yeni dosyalar ve klasörler bekleniyor...")
        
        print("Mevcut dosyalar taranıyor...")
        self.scan_existing()
        print("Tarama tamamlandı. İzleme modu aktif...")

        self.observer.schedule(self.handler, self.directory, recursive=False)
        self.observer.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """İzleme işlemini sonlandırır."""
        print("İzleyici durduruluyor...")
        self.observer.stop()
        self.observer.join()

    def scan_existing(self):
        """Başlangıçta mevcut dosyaları tarar ve düzenler."""
        if not os.path.exists(self.directory):
            print(f"Klasör bulunamadı: {self.directory}")
            return
            
        p = Path(self.directory)
        for item in p.iterdir():
            full_path = str(item)
            item_type = "Klasör" if item.is_dir() else "Dosya"
            print(f"[Mevcut {item_type} Bulundu]: {full_path}")
            
            if item.is_file() and self.organizer:
                self.organizer.organize_file(full_path)

if __name__ == "__main__":
    # Konfigürasyon dosyasını yükle
    current_file_path = Path(__file__).resolve()
    base_dir = current_file_path.parent.parent
    config_path = base_dir / 'config.json'
    
    target_dir = None
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                target_dir = config.get('source_directory')
        except Exception as e:
            print(f"Konfigürasyon hatası: {e}")

    # Hedef dizin kontrolü ve varsayılan atama
    if not target_dir or target_dir == "{gelecek}" or not os.path.exists(target_dir):
        print("Hedef dizin geçersiz. Test dizini kullanılıyor.")
        test_dir = base_dir / "test_folder"
        test_dir.mkdir(exist_ok=True)
        target_dir = str(test_dir)
        print(f"İzlenen Dizin: {target_dir}")
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

    # Düzenleyici sınıfını başlat
    organizer = None
    if HAS_ORGANIZER and 'config' in locals():
         try:
            organizer = FileOrganizer(config)
         except Exception as e:
             print(f"Organizer başlatılamadı: {e}")

    w = Watcher(target_dir, organizer)
    w.start()
