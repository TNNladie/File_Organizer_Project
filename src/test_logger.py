import time
from logger import get_logger 

def run_tests():
    print("--- TEST 1: Logger Başlatılıyor ---")
    log = get_logger()
    
    # 1. Normal Mesaj Testi
    print("-> Loglar basılıyor...")
    log.info("TEST: Sistem normal çalışıyor.")
    log.warning("TEST: Bu bir uyarı mesajıdır.")
    
    # Config dosyasında log_level 'INFO' ise bu görünmemeli:
    log.debug("TEST: Bu gizli bir debug mesajıdır.") 

    # 2. Exception (Hata) Yakalama Testi
    print("-> Hata yakalama testi yapılıyor...")
    try:
        # Bilerek hata oluşturuyoruz (Sıfıra bölme hatası)
        x = 1 / 0
    except Exception as e:
        # exc_info=True sayesinde hatanın tüm dökümü (traceback) loga düşmeli
        log.error("TEST: Kritik bir matematik hatası oluştu!", exc_info=True)

    # 3. Rotasyon (Rotation) Testi Simülasyonu
    # NOT: Bu kısım normalde 5MB dolana kadar çalışır. 
    # Test için logger kodundaki maxBytes değerini düşürüp denemek daha mantıklıdır.
    print("-> Test tamamlandı. Lütfen logs/ klasörünü kontrol et.")

if __name__ == "__main__":
    run_tests()