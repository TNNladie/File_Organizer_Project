import shutil
import time
import os
from pathlib import Path
from config_loader import load_config
from logger import get_logger
from reporter import generate_report

class Organizer:
    def __init__(self):
        # Config ve Logger yükle (Hata almamak için güvenli yükleme)
        self.config = load_config()
        self.logger = get_logger()
        
        self.source_dir = Path(self.config["source_directory"])
        self.dest_dir = Path(self.config["destination_directory"])
        self.extensions_map = self.config["file_extensions"]
        
        # Cleaner kontrolü
        try:
            from cleaner import sanitize_filename
            self.sanitize_filename = sanitize_filename
        except ImportError:
            self.sanitize_filename = lambda name: name.lower().replace(" ", "_")

    def _get_unique_path(self, target_folder, clean_name):
        """Generates a unique path to avoid overwriting existing files."""
        destination_path = target_folder / clean_name
        
        if not destination_path.exists():
            return destination_path
            
        counter = 1
        stem = Path(clean_name).stem
        suffix = Path(clean_name).suffix
        
        while True:
            new_name = f"{stem}_{counter}{suffix}"
            candidate_path = target_folder / new_name
            if not candidate_path.exists():
                return candidate_path
            counter += 1

    def organize_file(self, file_path):
        """Watcher için tekil dosya organizasyonu."""
        file_path = Path(file_path)
        
        # Temel kontroller
        if not file_path.exists() or file_path.is_dir():
            print(f"Atlandı (Klasör veya Yok): {file_path}")
            return False
            
        if file_path.suffix in ['.tmp', '.crdownload', '.part']:
            return False

        # 1. Kategori Bulma
        file_extension = file_path.suffix.lower()
        found_category = "Others"
        
        for category, extensions in self.extensions_map.items():
            if file_extension in extensions:
                found_category = category
                break
        
        # 2. Hedef Klasör
        target_folder = self.dest_dir / found_category
        target_folder.mkdir(parents=True, exist_ok=True)
        
        # 3. İsim Temizleme
        clean_name = self.sanitize_filename(file_path.name)
        destination_path = self._get_unique_path(target_folder, clean_name)
        
        # 4. Taşıma
        try:
            shutil.move(str(file_path), str(destination_path))
            
            log_msg = f"TASINDI | {found_category} | {file_path.name} -> {destination_path.name}"
            self.logger.info(log_msg)
            print(f"✔ [OK] {found_category}: {destination_path.name}")
            
            # --- Raporu Güncelle (Kullanıcı İsteği) ---
            try:
                generate_report()
            except Exception as e:
                print(f"Rapor güncellenemedi: {e}")
                
            return True
            
        except PermissionError:
            self.logger.error(f"ERİŞİM HATASI | {file_path.name} dosyası kullanımda.")
        except Exception as e:
            self.logger.error(f"HATA | {file_path.name} taşınamadı: {e}")
        
        return False

    def scan_directory(self):
        """Main.py seçeneği için toplu tarama."""
        print(f"📂 Klasör Taranıyor: {self.source_dir}")
        print("-" * 50)
        
        if not self.source_dir.exists():
            print("HATA: Kaynak klasör bulunamadı!")
            return

        count = 0
        for item in self.source_dir.iterdir():
            if item.is_file():
                if self.organize_file(item):
                    count += 1
                
        print("-" * 50)
        print(f"✨ Tarama Bitti. Toplam işlem gören: {count}")

# Backward compatibility (Main.py veya Watcher.py uyumu)
if __name__ == "__main__":
    organizer = Organizer()
    organizer.scan_directory()
