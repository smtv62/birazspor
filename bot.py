import requests
import re
import time

def get_updated_bot():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
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

    try:
        # 1. Ana siteden aktif xyz linkini çek
        print("Ana site taranıyor...")
        main_res = requests.get("https://birazcikspor.com", headers=headers, timeout=15)
        # 'Canlı Maç Girişi' linkini bul (href içinde xyz geçen linki yakala)
        match_main = re.search(r'href="(https?://birazcikspor[^"]+\.xyz)"', main_res.text)
        
        if match_main:
            active_domain = match_main.group(1).rstrip('/')
            print(f"Aktif site bulundu: {active_domain}")
        else:
            # Eğer otomatik bulamazsa senin verdiğin sabit adresi kullan
            active_domain = "https://birazcikspor44.xyz"
            print(f"Aktif site otomatik bulunamadı, varsayılan kullanılıyor: {active_domain}")

        m3u_content = "#EXTM3U\n"
        found_count = 0

        for ch in channels:
            event_url = f"{active_domain}/event.html?id={ch}"
            try:
                # İsteği yaparken tarayıcı gibi davranıyoruz
                res = requests.get(event_url, headers=headers, timeout=10)
                
                # 'const baseurl' satırını daha geniş bir regex ile arıyoruz
                match_url = re.search(r'const\s+baseurl\s*=\s*["\'](https?://[^"\']+)["\']', res.text)
                
                if match_url:
                    base_url = match_url.group(1)
                    # M3U8 linkini oluştur (Örn: https://.../checklist/androstreamlivebiraz1.m3u8)
                    stream_link = f"{base_url}{ch}.m3u8"
                    
                    m3u_content += f"#EXTINF:-1, {ch}\n{stream_link}\n"
                    print(f"Başarılı: {ch}")
                    found_count += 1
                else:
                    print(f"Kaynak bulunamadı: {ch}")
                
                # Siteyi yormamak ve banlanmamak için kısa bir bekleme
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Kanal hatası {ch}: {e}")
                continue

        # Dosyayı kaydet
        with open("liste.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_content)
        
        print(f"İşlem tamamlandı. Toplam {found_count} kanal eklendi.")

    except Exception as e:
        print(f"Genel hata: {e}")

if __name__ == "__main__":
    get_updated_bot()
