import os
import json
import shutil # Dosya taşıma işlemi için gerekli

# KLASÖR OLUŞTURMA FONKSİYON
def klasor_olustur(klasor_yolu):
    if not os.path.exists(klasor_yolu):
        os.makedirs(klasor_yolu) #adresteki klasör oluşturur "Duzenli_Dosyalar klasörünü inşa eder.""
        print(f"Yeni klasör oluşturuldu: {klasor_yolu}")

# İSİM YAPMA FONKSİYON
def Farkli_isim_yap(hedef_klasor, dosya_adi):
    dosya_adi = dosya_adi.replace(" ", "_")
    isim, uzanti = os.path.splitext(dosya_adi) 

    sayac = 1
    yeni_yol = os.path.join(hedef_klasor, dosya_adi)

    while os.path.exists(yeni_yol):
        yeni_isim = f"{isim}_{sayac}{uzanti}"
        yeni_yol = os.path.join(hedef_klasor, yeni_isim)
        sayac = sayac + 1
        
    return os.path.basename(yeni_yol)

# TAŞIMA FONKSİYONU
def dosyayi_duzenle(dosya_yolu, ayarlar):
    try:
        dosya_adi = os.path.basename(dosya_yolu)
        uzanti = os.path.splitext(dosya_adi)[1].lower()
        gidecegi_kategori = "Diger" #eşleşme olmaz ise böyle bir klasör oluşturur ve oraya atar.

        if "file_extensions" in ayarlar:
            for kategori, uzanti_listesi in ayarlar["file_extensions"].items():
                if uzanti in uzanti_listesi:
                    gidecegi_kategori = kategori
                    break 
        
    
        ana_hedef_tam = ayarlar.get("destination_directory", ayarlar.get("destination_folder"))
        
        if not ana_hedef_tam or ana_hedef_tam == "{gelecek}":
            print("Hata: Hedef klasör ayarı bulunamadı (destination_directory).")
            return

        ana_hedef= os.path.expanduser(ana_hedef_tam) #~ işaretini açar 
        hedef_klasor = os.path.join(ana_hedef, gidecegi_kategori) #hedef klasör yolunu oluşturur
    
        klasor_olustur(hedef_klasor)
        

        yeni_dosya_adi = Farkli_isim_yap(hedef_klasor, dosya_adi)
        
        son_hedef_yol = os.path.join(hedef_klasor, yeni_dosya_adi)
        
        shutil.move(dosya_yolu, son_hedef_yol)#dosyayı taşıma işlemi kütüphanesi
        
        print(f"Başarılı: {dosya_adi} -> {gidecegi_kategori} olarak taşındı.")
        
    except Exception as hata:
        print(f"Hata oluştu: {hata}")

dosyayi_duzenle("C:\Users\tuana\Downloads",CONFIG)