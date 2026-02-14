import os
import json
from pathlib import Path
import shutil


class Organizer:
    """
    Ana motor: Filtreleri uygular ve dosyaları dağıtır.
    """
    def __init__(self, config_path="config.json"):
        # Config dosyasını yükle
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                self.CONFIG = json.load(f)
        except FileNotFoundError:
            # Yedek varsayılan konfigürasyon (config.json bulunamazsa)
            self.CONFIG = {
                "file_extensions": {
                    "Images": [".jpg", ".jpeg", ".png", ".gif"],
                    "Documents": [".pdf", ".docx", ".txt", ".xlsx"],
                    "Videos": [".mp4", ".mkv"],
                    "Music": [".mp3", ".wav"],
                    "Archives": [".zip", ".rar"]
                }
            }

        self.FILE_EXTENSIONS = self.CONFIG["file_extensions"]
        self.FILES = list(self.FILE_EXTENSIONS.keys())  # Hedef klasör listesi

    def create_directory(self, target_path):
        """Hedef klasörleri oluşturur."""
        if not os.path.exists(target_path):
            os.makedirs(target_path)

    def get_unique_name(self, path, filename):
        """Eğer dosya hedefte varsa sonuna _1, _2 ekleyerek benzersiz isim üretir."""
        base, extension = os.path.splitext(filename)
        counter = 1
        unique_name = filename
        while os.path.exists(os.path.join(path, unique_name)):
            unique_name = f"{base}_{counter}{extension}"
            counter += 1
        return unique_name

    def clean_filename(self, filename):
        """Boşlukları ve özel karakterleri '_' ile değiştirir, küçük harf yapar ve ardışık '_' işaretlerini teke indirir."""
        import re
        name, ext = os.path.splitext(filename)
        # Sadece harf ve sayıları tut, geri kalanı _ yap
        clean_name = re.sub(r'[^a-zA-Z0-9]', '_', name.lower())
        # Ardışık alt tireleri teke indir
        clean_name = re.sub(r'_+', '_', clean_name).strip('_')
        return f"{clean_name}{ext.lower()}"

    def move_file(self, source_dir, dest_dir=None):
        """
        Dosyaları source_dir'den taşır. 
        dest_dir verilmişse oraya taşır, verilmemişse source_dir içinde kategorize eder.
        JSON'da tanımlı olmayan uzantılar 'Others' klasörüne gider.
        """
        source_path = Path(source_dir)
        moved_count = 0
        
        if not source_path.exists():
            print(f"Hata: Kaynak dizin bulunamadı: {source_dir}")
            return 0

        # Klasördeki tüm nesneleri tara
        items = os.listdir(source_path)
        if not items:
            print("Klasör boş.")
            return 0

        for item in items:
            item_path = source_path / item

            # Klasörleri atla, sadece dosyaları organize et
            if os.path.isdir(item_path):
                continue

            # 1. Dosya adını ve uzantısını al
            filename = item
            extension = os.path.splitext(filename)[1].lower()

            # 2. Hedef klasörü belirle
            target_folder_name = "Others"  # Varsayılan: Diğer
            found = False
            for folder, exts in self.FILE_EXTENSIONS.items():
                if extension in exts:
                    target_folder_name = folder
                    found = True
                    break
            
            # Eğer uzantı JSON içinde yoksa target_folder_name zaten "Others" kalır.

            # Hedef ana yolu belirle (Ya belirli bir yer ya da kaynağın içi)
            base_dest = Path(dest_dir) if dest_dir else source_path
            target_dir = base_dest / target_folder_name
            
            # 3. Klasör yoksa oluştur (Sizin istediğiniz 'yoksa oluştursun' kısmı)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            # 4. Dosya adını temizle (Opsiyonel: İsteğe göre kapatılabilir)
            cleaned_name = self.clean_filename(filename)
            
            # İsim çakışmasını önle
            final_name = self.get_unique_name(target_dir, cleaned_name)
            final_path = target_dir / final_name

            # 5. Taşıma işlemini gerçekleştir
            try:
                shutil.move(item_path, final_path)
                status = "Bulundu" if found else "Bilinmiyor -> Others"
                print(f"[{status}] Taşındı: {filename} -> {target_folder_name}/{final_name}")
                moved_count += 1
            except Exception as e:
                print(f"Hata: {filename} taşınırken sorun oluştu: {e}")
        
        return moved_count


    def get_preview(self, source_dir, dest_dir=None):
        """
        Taşınacak dosyaların bir listesini döndürür (aslında taşımaz).
        Dönen liste: [{'filename': ..., 'target_folder': ..., 'extension': ..., 'path': ...}]
        """
        source_path = Path(source_dir)
        preview_list = []
        
        if not source_path.exists():
            return []

        for item in os.listdir(source_path):
            item_path = source_path / item
            if os.path.isdir(item_path):
                continue

            extension = os.path.splitext(item)[1].lower()
            target_folder_name = "Others"
            for folder, exts in self.FILE_EXTENSIONS.items():
                if extension in exts:
                    target_folder_name = folder
                    break
            
            preview_list.append({
                "filename": item,
                "target_folder": target_folder_name,
                "extension": extension,
                "path": str(item_path)
            })
        
        return preview_list

    def move_specific_files(self, file_list, dest_dir=None):
        """
        Sadece listedeki belirli dosyaları taşır.
        file_list: list of dicts with 'path' and 'target_folder'
        """
        moved_count = 0
        for file_info in file_list:
            item_path = Path(file_info["path"])
            if not item_path.exists():
                continue
                
            target_folder_name = file_info["target_folder"]
            # Hedef dizini belirle
            base_dest = Path(dest_dir) if dest_dir else item_path.parent
            target_dir = base_dest / target_folder_name
            
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            cleaned_name = self.clean_filename(item_path.name)
            final_name = self.get_unique_name(target_dir, cleaned_name)
            final_path = target_dir / final_name

            try:
                shutil.move(item_path, final_path)
                moved_count += 1
            except Exception as e:
                print(f"Taşıma hatası: {e}")
        
        return moved_count


if __name__ == "__main__":
    # Test amaçlı doğrudan çalıştırma
    organizer = Organizer()
    test_dir = Path.home() / "Downloads"
    organizer.move_file(test_dir)
