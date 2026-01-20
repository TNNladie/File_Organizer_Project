import sys
# Diğer modülleri import et
# from organizer import run_organizer_scan
from watcher import start_watching
from reporter import generate_report

def main():
    print("DOSYA DÜZENLEME OTOMASYONU v1.0")
    print("1. Mevcut Klasörü Düzenle (Tara ve Taşı)")
    print("2. Otomatik İzlemeyi Başlat (Watcher Modu)")
    print("3. Rapor Al")
    print("4. Çıkış")
    
    secim = input("Seçiminiz (1-4): ")
    
    if secim == '1':
        print("Tarama başlıyor...")
        # run_organizer_scan() -> yerine:
        from organizer import Organizer
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