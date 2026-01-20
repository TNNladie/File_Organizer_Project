import logging
import sys
from pathlib import Path
from config_loader import load_config

def get_logger(name="OrganizerLogger"):
    """
    Konfigürasyondaki ayara göre bir logger döner.
    Hem dosyaya hem de konsola log basar.
    """
    config = load_config()
    log_file_path = config.get("log_file_path", "organizer.log")

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Eğer daha önce handler eklendiyse tekrar ekleme (Multiprocess/import sismesi onlemi)
    if logger.hasHandlers():
        return logger

    # Format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # 1. Dosya Handler
    try:
        file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"Log dosyası oluşturulamadı: {e}")

    # 2. Konsol Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

if __name__ == "__main__":
    log = get_logger()
    log.info("Logger test mesajı: Sistem çalışıyor.")