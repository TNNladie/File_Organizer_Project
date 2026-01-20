import sys
import os

# src klasörünü path'e ekle (Modüllerin birbirini bulması için)
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.append(src_dir)

from watcher import start_watching
from reporter import generate_report
from organizer import Organizer

def main():
    print("DOSYA DÜZENLEME OTOMASYONU v1.0")
    print("1. Mevcut Klasörü Düzenle (Tara ve Taşı)")
    print("2. Otomatik İzlemeyi Başlat (Watcher Modu)")
    print("3. Rapor Al")
    print("4. Çıkış")
    
    secim = input("Seçiminiz (1-4): ")
    
    if secim == '1':
        print("Tarama başlıyor...")
        org = Organizer()
        org.scan_directory()
    elif secim == '2':
        start_watching()
    elif secim == '3':
        generate_report()
    elif secim == '4':
        sys.exit()
    else:
        print("Geçersiz seçim.")

if __name__ == "__main__":
    main()