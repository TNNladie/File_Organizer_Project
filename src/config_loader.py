import json
import os
import sys
from pathlib import Path

# Proje kök dizinini bul: src'nin bir üstü
ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE_PATH = ROOT_DIR / "config.json"

def get_default_downloads_folder():
    """İşletim sistemine göre İndirilenler klasörünü bulur."""
    return str(Path.home() / "Downloads")

def load_config():
    """Config dosyasını okur ve ayarları döner."""
    if not CONFIG_FILE_PATH.exists():
        print(f"KRİTİK HATA: Config dosyası bulunamadı!")
        print(f"Aranan Yer: {CONFIG_FILE_PATH}")
        sys.exit(1)

    try:
        with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as file:
            config = json.load(file)
            
            user_downloads = get_default_downloads_folder()
            
            # {gelecek} yer tutucularını değiştir
            if config.get("source_directory") == "{gelecek}":
                config["source_directory"] = user_downloads     
            if config.get("destination_directory") == "{gelecek}":
                config["destination_directory"] = user_downloads

            # Log klasörünü de ana dizinde (logs) oluştur
            log_dir = ROOT_DIR / "logs"
            log_dir.mkdir(exist_ok=True)
            
            # Path objesini string'e çevirerek kaydet
            config["log_file_path"] = str(log_dir / config.get("log_file", "organizer.log"))

            return config

    except Exception as e:
        print(f"Hata: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print(f"Proje Ana Dizini: {ROOT_DIR}")
    c = load_config()
    print("Konfigürasyon başarıyla yüklendi.")
