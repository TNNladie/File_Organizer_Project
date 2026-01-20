import time
import logging
import os
import json
import sys
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Modül bağımlılıklarını yönet (Import işlemleri)
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
    # Dosya sistemi olaylarını işleyen sınıf
    def __init__(self, organizer=None):
        self.organizer = organizer

    def on_created(self, event):
        # Dosya veya klasör oluşturulduğunda tetiklenir
        path_type = "KLASÖR" if event.is_directory else "DOSYA"
        src_path_str = str(event.src_path)
        
        message = f"!!! YENİ {path_type} TESPİT EDİLDİ: {src_path_str} !!!"
        print(message)
        logging.info(message)
        
        # Dosya yazma işleminin bitmesi için bekle
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
    # İzleme ve değişiklik yönetimi ana sınıfı
    def __init__(self, directory, organizer=None):
        self.directory = str(Path(directory).resolve())
        self.organizer = organizer
        self.observer = Observer()
        self.handler = WatcherHandler(organizer)

    def start(self):
        # İzleme işlemini başlat
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
        # İzlemeyi durdur
        print("İzleyici durduruluyor...")
        self.observer.stop()
        self.observer.join()

    def scan_existing(self):
        # Başlangıçta mevcut dosyaları tara ve düzenle
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
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    
    # Kullanıcıdan izlenecek klasör yolunu al
    print("--- Dosya İzleyici ve Düzenleyici ---")
    
    target_dir = None
    while not target_dir:
        user_input = input("Lütfen izlenecek klasör yolunu girin: ").strip()
        user_input = user_input.strip('"').strip("'")  # Tırnakları temizle
        
        if os.path.exists(user_input) and os.path.isdir(user_input):
            target_dir = user_input
        else:
            print("! Geçersiz klasör yolu veya klasör bulunamadı. Lütfen tekrar deneyin.")

    print(f"\nSeçilen Hedef Dizin: {target_dir}")

    # Yapılandırmayı yükle
    current_file_path = Path(__file__).resolve()
    base_dir = current_file_path.parent.parent
    config_path = base_dir / 'config.json'
    
    organizer = None
    if HAS_ORGANIZER:
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    organizer = FileOrganizer(config)
                    print("-> Organizer modülü aktif.")
            except Exception as e:
                print(f"-> Config hatası: {e}")
                print("-> Organizer devre dışı.")
        else:
            print("-> Config dosyası yok. Organizer devre dışı.")
    else:
        print("-> Organizer modülü yok.")

    # İzleyiciyi başlat
    w = Watcher(target_dir, organizer)
    w.start()
