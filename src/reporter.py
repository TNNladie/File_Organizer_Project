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
        
        report_lines = []
        report_lines.append("=" * 40)
        report_lines.append(f" TOPLAM TAŞINAN DOSYA SAYISI: {total_moved}")
        report_lines.append("=" * 40)
        report_lines.append("KATEGORİ DAĞILIMI:")
        report_lines.append("-" * 40)
        for cat, count in categories.most_common():
            report_lines.append(f" {cat:<20} : {count}")
        report_lines.append("-" * 40)
        report_lines.append("Rapor sonu.\n")

        # Hem ekrana yaz hem dosyaya kaydet
        output_text = "\n".join(report_lines)
        print(output_text)
        
        with open("report.txt", "w", encoding="utf-8") as report_file:
            report_file.write(f"--- RAPOR --- (Kaynak: {log_path})\n")
            report_file.write(output_text)
        
        print(f"\n>> Rapor dosyası oluşturuldu: {os.path.abspath('report.txt')}")

    except Exception as e:
        print(f"Rapor oluşturulurken hata: {e}")

if __name__ == "__main__":
    generate_report()