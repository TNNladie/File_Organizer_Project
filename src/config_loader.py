# Dosya: src/config_loader.py
import json
import os
from pathlib import Path

def load_config():
    """
    Projenin ana dizinindeki config.json dosyasını yükler.
    src klasörünün bir üstüne çıkarak dosyayı arar.
    """
    # Şu anki dosyanın (config_loader.py) olduğu yerin bir üst klasörünü (root) bul
    base_dir = Path(__file__).resolve().parent.parent
    config_path = base_dir / 'config.json'

    # Eğer config.json yoksa varsayılan boş bir ayar döndür
    if not config_path.exists():
        print(f"UYARI: Config dosyası bulunamadı: {config_path}")
        return {}

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Config dosyası okunurken hata oluştu: {e}")
        return {}