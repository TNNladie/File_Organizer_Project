import re
import unicodedata

def sanitize_filename(filename):
    """
    Dosya ismini temizler:
    1. Türkçe karakterleri İngilizceye çevirir (ç -> c, ş -> s).
    2. Boşlukları alt tire (_) ile değiştirir.
    3. Alfanümerik olmayan (nokta ve tire hariç) karakterleri siler.
    """
    # Dosya adı ve uzantısını ayır
    if '.' in filename:
        name, ext = filename.rsplit('.', 1)
        ext = f".{ext}"
    else:
        name = filename
        ext = ""
    
    # 1. Unicode Normalizasyonu (Türkçe karakter düzeltme)
    # Örn: "ödev" -> "odev"
    name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('utf-8')
    
    # 2. İstenmeyen karakterleri sil (Sadece harf, rakam, - ve _ kalsın)
    name = re.sub(r'[^\w\s-]', '', name)
    
    # 3. Boşlukları _ yap
    name = re.sub(r'[-\s]+', '_', name).strip('-_')
    
    return f"{name}{ext}"