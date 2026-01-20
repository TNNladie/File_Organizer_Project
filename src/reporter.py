import os
from collections import Counter
from config_loader import load_config

def generate_report():
    config = load_config()
    log_path = config.get("log_file_path", "organizer.log")
    
    if not os.path.exists(log_path):
        print(f"Log dosyası bulunamadı: {log_path}")
        return

    total_moved = 0
    categories = Counter()

    print(f"\n--- RAPOR OLUŞTURULUYOR ---")
    print(f"Kaynak Log: {log_path}\n")

    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            for line in f:
                if "TASINDI" in line:
                    total_moved += 1
                    # Log format: ... - TASINDI | Category | File -> ...
                    parts = line.split("|")
                    if len(parts) >= 2:
                        category = parts[1].strip()
                        categories[category] += 1
        
        print("=" * 40)
        print(f" TOPLAM TAŞINAN DOSYA SAYISI: {total_moved}")
        print("=" * 40)
        print("KATEGORİ DAĞILIMI:")
        print("-" * 40)
        for cat, count in categories.most_common():
            print(f" {cat:<20} : {count}")
        print("-" * 40)
        print("Rapor sonu.\n")

    except Exception as e:
        print(f"Rapor oluşturulurken hata: {e}")

if __name__ == "__main__":
    generate_report()