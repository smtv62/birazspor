import requests
import re
import time

def get_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://birazcikspor.com/'
    }
    
    channels = [
        "androstreamlivebiraz1", "androstreamlivebs1", "androstreamlivebs2", "androstreamlivebs3",
        "androstreamlivebs4", "androstreamlivebs5", "androstreamlivebsm1", "androstreamlivebsm2",
        "androstreamlivess1", "androstreamlivess2", "androstreamlivets", "androstreamlivets1",
        "androstreamlivets2", "androstreamlivets3", "androstreamlivets4", "androstreamlivesm1",
        "androstreamlivesm2", "androstreamlivees1", "androstreamlivees2", "androstreamlivetb",
        "androstreamlivetb1", "androstreamlivetb2", "androstreamlivetb3", "androstreamlivetb4",
        "androstreamlivetb5", "androstreamlivetb6", "androstreamlivetb7", "androstreamlivetb8",
        "androstreamliveexn", "androstreamliveexn1", "androstreamliveexn2", "androstreamliveexn3",
        "androstreamliveexn4", "androstreamliveexn5", "androstreamliveexn6", "androstreamliveexn7",
        "androstreamliveexn8"
    ]

    active_domain = "https://birazcikspor44.xyz" # Burayı gerekirse ana siteden çekebiliriz
    m3u_content = "#EXTM3U\n"
    found_base_url = None

    print(f"Kaynak aranıyor: {active_domain}")

    # Önce tek bir kanaldan baseurl'yi çekmeye çalışalım (Hepsinde aynıdır)
    test_url = f"{active_domain}/event.html?id=androstreamlivebiraz1"
    try:
        res = requests.get(test_url, headers=headers, timeout=10)
        # JS içindeki baseurls dizisini yakala
        # Regex: baseurls = [ "URL" ] yapısını arar
        urls = re.findall(r'https?://[a-zA-Z0-9.-]+\.[a-z]{2,}/checklist/', res.text)
        
        if urls:
            found_base_url = urls[0]
            print(f"Base URL bulundu: {found_base_url}")
        else:
            # Eğer doğrudan HTML'de yoksa, sayfada yüklü olan JS dosyalarını kontrol etmemiz gerekebilir
            print("Base URL bulunamadı, alternatif metod deneniyor...")
            # Bazen asıl kod player.js gibi bir dosyadadır.
    except Exception as e:
        print(f"Bağlantı hatası: {e}")

    if found_base_url:
        for ch in channels:
            # İstediğin format: baseurl + kanal_id + .m3u8
            final_link = f"{found_base_url}{ch}.m3u8"
            m3u_content += f"#EXTINF:-1, {ch}\n{final_link}\n"
        
        with open("liste.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_content)
        print("Liste başarıyla oluşturuldu.")
    else:
        print("Kritik Hata: Base URL hiçbir şekilde yakalanamadı!")

if __name__ == "__main__":
    get_data()
