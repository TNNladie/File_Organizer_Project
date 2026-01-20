import logging
import sys
import os
from pathlib import Path
from config_loader import load_config

def get_logger(name="OrganizerLogger"):
    """
    Konfigürasyondaki ayara göre bir logger döner.
    Hem dosyaya hem de konsola log basar.
    """
    config = load_config()
    # Varsayılan yol logs altına alındı
    log_file_path = config.get("log_file_path", "logs/organizer.log")
    
    # Log seviyesini Config dosyasından dinamik okuma (Debug/Info ayrımı için)
    config_level = config.get("log_level", "INFO").upper()
    log_level = getattr(logging, config_level, logging.INFO)
    
    logger = logging.getLogger(name)
    logger.setLevel(log_level) # Değişken kullanıldı

    # Eğer daha önce handler eklendiyse tekrar ekleme (Multiprocess/import sismesi onlemi)
    if logger.hasHandlers():
        return logger
    
    # Eğer 'logs' klasörü yoksa otomatik oluşturmak için
    log_dir = os.path.dirname(log_file_path)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Format
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 1. Dosya Handler
    try:
        file_handler = logging.FileHandler(
            log_file_path, 
            maxBytes=5*1024*1024, # Dosya boyutunun çok büyüdüğü durumlar için
            backupCount=3, # Eski log dosyalarını yedekte tutuyoruz
            encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"Log dosyası oluşturulamadı: {e}")

    # 2. Konsol Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    logger.addHandler(console_handler)

    return logger

if __name__ == "__main__":
    log = get_logger()
    log.info("Logger test mesajı: Sistem çalışıyor.")