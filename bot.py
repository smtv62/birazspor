import requests
import re
import time

def generate_iptv_list():
    # Yayıncı sunucunun beklediği kimlik bilgileri
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    referer = "https://birazcikspor44.xyz/" # Ana yayıncı domaini
    
    headers = {
        'User-Agent': user_agent,
        'Referer': 'https://birazcikspor.com/'
    }

    # Statik kanal ID listesi (Siteden isimlerini çekeceğiz)
    channel_ids = [
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
        # 1. Aktif Domaini Bul
        main_page = requests.get("https://birazcikspor.com", headers=headers, timeout=15).text
        active_site_match = re.search(r'href="(https?://birazcikspor[^"]+\.xyz)"', main_page)
        active_domain = active_site_match.group(1).rstrip('/') if active_site_match else "https://birazcikspor44.xyz"

        # 2. BaseURL'yi Çek (Checklist Linki)
        sample_url = f"{active_domain}/event.html?id=androstreamlivebiraz1"
        sample_res = requests.get(sample_url, headers=headers, timeout=15).text
        base_urls = re.findall(r'"(https?://[^"]+/checklist/)"', sample_res)
        
        if not base_urls:
            print("BaseURL bulunamadı!")
            return
        
        final_base = base_urls[0]
        
        # 3. M3U İçeriğini Oluştur (Referer ve User-Agent Ekleyerek)
        m3u_output = "#EXTM3U\n"
        
        for cid in channel_ids:
            # Kanalın düzgün ismini ID'den türetelim veya "Kanal" ekleyelim
            # Örn: androstreamlivebs1 -> BS 1
            display_name = cid.replace("androstreamlive", "").upper
