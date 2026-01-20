import os
import json
from pathlib import Path
import shutil


class Organizer:
    def __init__(self):
        self.BASE_DIR = Path.home()
        self.DOWNLOADS_DIR = self.BASE_DIR / "Downloads"

        # Config dosyasını yükle
        with open("../config.json", "r", encoding="utf-8") as f:
            self.CONFIG = json.load(f)

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
        """Boşlukları '_' ile değiştirir ve küçük harf yapar."""
        name, ext = os.path.splitext(filename)
        clean_name = name.lower().replace(" ", "_")
        return f"{clean_name}{ext.lower()}"

    def move_file(self, source_dir):
        # Klasördeki tüm dosyaları tara
        for item in os.listdir(source_dir):
            item_path = source_dir / item

            # Klasörleri değil sadece dosyaları işle
            if os.path.isdir(item_path):
                continue

            # 1. Dosya adını temizle (Boşluk -> Alt Tire)
            cleaned_name = self.clean_filename(item)
            extension = os.path.splitext(item)[1].lower()

            # 2. Uzantıya göre hedef klasörü belirle
            target_folder_name = "Others"  # Varsayılan klasör
            for folder, exts in self.FILE_EXTENSIONS.items():
                if extension in exts:
                    target_folder_name = folder
                    break

            target_dir = source_dir / target_folder_name
            self.create_directory(target_dir)

            # 3. İsim çakışmasını önle (Aynı isimde dosya varsa)
            final_name = self.get_unique_name(target_dir, cleaned_name)
            final_path = target_dir / final_name

            # 4. Taşıma işlemini gerçekleştir
            shutil.move(item_path, final_path)
            print(f"Taşındı: {item} -> {target_folder_name}/{final_name}")


if __name__ == "__main__":
    organizer = Organizer()
    organizer.move_file(organizer.DOWNLOADS_DIR)