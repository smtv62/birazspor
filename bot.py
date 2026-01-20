import requests
import re
import os

def generate_iptv_list():
    # Tarayıcı gibi görünmek için Header
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://birazcikspor.com/'
    }

    channel_list = [
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
        # 1. Adım: Aktif siteyi bul
        print("Ana site kontrol ediliyor...")
        main_page = requests.get("https://birazcikspor.com", headers=headers, timeout=15).text
        active_site_match = re.search(r'href="(https?://birazcikspor[^"]+\.xyz)"', main_page)
        
        active_domain = active_site_match.group(1) if active_site_match else "https://birazcikspor44.xyz"
        print(f"Hedef Site: {active_domain}")

        # 2. Adım: Kaynak koda gir ve baseurls dizisini ayıkla
        # Herhangi bir kanalın id'si ile sayfaya gidiyoruz
        target_url = f"{active_domain}/event.html?id=androstreamlivebiraz1"
        response = requests.get(target_url, headers=headers, timeout=15)
        
        # Regex ile tırnak içindeki checklist linklerini buluyoruz
        base_urls = re.findall(r'"(https?://[^"]+/checklist/)"', response.text)

        if not base_urls:
            print("HATA: Kaynak kodunda baseurl bulunamadı!")
            return

        # İlk bulunan baseurl'yi alıyoruz
        final_base = base_urls[0]
        print(f"Yayın Kaynağı Bulundu: {final_base}")

        # 3. Adım: M3U Dosyasını Oluştur
        m3u_output = "#EXTM3U\n"
        for channel in channel_list:
            # Format: baseurl + kanal_id + .m3u8
            link = f"{final_base}{channel}.m3u8"
            m3u_output += f"#EXTINF:-1, {channel}\n{link}\n"

        with open("liste.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_output)
        
        print(f"Bitti! 'liste.m3u' dosyasına {len(channel_list)} kanal yazıldı.")

    except Exception as e:
        print(f"Bir hata oluştu: {e}")

if __name__ == "__main__":
    generate_iptv_list()
