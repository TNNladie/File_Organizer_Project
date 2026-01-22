# Smart File Organizer v2.0

İndirilenler klasörünüzü saniyeler içinde düzene sokan, modern arayüzlü ve akıllı bir dosya düzenleme otomasyonudur. Dosyalarınızı türlerine göre (Resimler, Belgeler, Kodlar, Videolar vb.) otomatik olarak kategorize eder ve detaylı raporlar sunar.

## Öne Çıkan Özellikler

* **Hemen Organize Et:** Mevcut tüm dosyaları tek tıkla tarar ve türlerine göre ilgili klasörlere taşır.
* **Otomatik İzle (Watcher):** Arka planda çalışarak klasöre yeni gelen her dosyayı anında yakalar ve saniyesinde yerini değiştirir.
* **Görsel Raporlama:** Uygulama içindeki arayüzde, hem sistem genelini hem de o anki klasörü kapsayan ASCII çubuk grafikli raporlar sunar.
* **Akıllı İsimlendirme:** Dosyaları taşırken Türkçe karakterleri temizler ve aynı isimde dosya varsa üzerine yazmak yerine benzersiz isimler oluşturur.

---

## Nasıl Kullanılır?

### 1. Yöntem: Doğrudan Kullanım (Hızlı Kurulum)
Herhangi bir yazılım bilgisi veya Python kurulumu gerektirmeden kullanmak için:
1.  Bu sayfanın sağ tarafındaki **"Releases"** bölümüne gidin.
2.  En güncel sürümdeki `Smart_File_Organizer_v2.exe` dosyasını indirin.
3.  Dosyayı çalıştırın. 
    > *Not: Windows Defender "Bilinmeyen Yayıncı" uyarısı verebilir. "Ek Bilgi" butonuna tıklayıp "Yine de Çalıştır" diyerek uygulamayı başlatabilirsiniz.*

### 2. Yöntem: Terminal / Geliştirici Modu
Projeyi kaynak koddan çalıştırmak veya geliştirmek isterseniz:
1.  **Depoyu Klonlayın:**
    ```bash
    git clone https://github.com/TNNladie/File_Organizer_Project.git
    cd File_Organizer_Project
    ```
2.  **Bağımlılıkları Kurun:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Uygulamayı Başlatın:**
    ```bash
    python app_gui.py
    ```

---

## ⚙️ Yapılandırma (config.json)
Program varsayılan olarak sisteminizin **İndirilenler (Downloads)** klasörünü hedef alır. Ayarları özelleştirmek için ana dizindeki `config.json` dosyasını kullanabilirsiniz:
* `file_extensions`: Hangi uzantının hangi klasör ismine gideceğini tanımlar.
* `source_directory`: Taranacak ana klasör yoludur (Varsayılan: `{path}` sistem klasörünü temsil eder).



## 🛠️ Kullanılan Teknolojiler
* **Python**
* **CustomTkinter:** Modern ve karanlık mod destekli kullanıcı arayüzü.
* **Watchdog:** Gerçek zamanlı dosya sistemi takibi.
* **PyInstaller:** Tek dosyalık `.exe` paketleme sistemi.
