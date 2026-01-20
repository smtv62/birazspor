import requests
import re
import os

def get_data():
    base_entry_url = "https://birazcikspor.com"
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
        # 1. Adım: Ana siteden aktif yönlendirme adresini bul (Canlı Maç Girişi)
        response = requests.get(base_entry_url, timeout=10)
        # Burada sitenin yapısına göre asıl domaini (xyz'li olanı) çekiyoruz. 
        # Örnek olarak yönlendirmeyi manuel veya regex ile yakalayabilirsin.
        # Şimdilik senin verdiğin güncel domain üzerinden devam ediyoruz:
        active_domain = "https://birazcikspor44.xyz" 

        m3u_content = "#EXTM3U\n"

        for ch in channels:
            event_url = f"{active_domain}/event.html?id={ch}"
            try:
                res = requests.get(event_url, timeout=5)
                # 2. Adım: Kaynak kodundan baseurl yakala
                # Örn: const baseurl = "https://andro.226503.xyz/checklist/";
                match = re.search(r'const baseurl = "(https?://[^"]+)"', res.text)
                
                if match:
                    stream_link = match.group(1)
                    # IPTV Formatına ekle
                    m3u_content += f"#EXTINF:-1,{ch}\n{stream_link}{ch}.m3u8\n"
                    print(f"Bulundu: {ch}")
            except:
                continue

        # 3. Adım: Dosyaya yaz
        with open("liste.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_content)

    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    get_data()
