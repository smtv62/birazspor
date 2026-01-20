import requests
import re
import os

def generate_iptv_list():
    # Kimlik Bilgileri
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    
    headers = {
        'User-Agent': user_agent,
        'Referer': 'https://birazcikspor.com/'
    }

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
        print("Site taranıyor...")
        main_res = requests.get("https://birazcikspor.com", headers=headers, timeout=15)
        active_site_match = re.search(r'href="(https?://birazcikspor[^"]+\.xyz)"', main_res.text)
        active_domain = active_site_match.group(1).rstrip('/') if active_site_match else "https://birazcikspor44.xyz"
        print(f"Hedef Site: {active_domain}")

        # 2. BaseURL'yi Çek
        # Sayfa kaynağındaki 'const baseurls = [...]' kısmından linki çekiyoruz
        sample_url = f"{active_domain}/event.html?id=androstreamlivebiraz1"
        sample_res = requests.get(sample_url, headers=headers, timeout=15).text
        # Hem tek tırnak hem çift tırnak destekleyen regex
        base_urls = re.findall(r'["\'](https?://[^"\']+/checklist/)["\']', sample_res)
        
        if not base_urls:
            print("HATA: BaseURL (checklist) bulunamadı!")
            return
        
        final_base = base_urls[0]
        print(f"Kaynak URL: {final_base}")

        # 3. M3U İçeriğini Oluştur
        m3u_output = "#EXTM3U\n"
        
        for cid in channel_ids:
            # İsim temizleme: androstreamlivebs1 -> BS1
            clean_name = cid.replace("androstreamlive", "").upper()
            stream_url = f"{final_base}{cid}.m3u8"
            
            # Oynatıcılar için Header bilgilerini ekle
            m3u_output += f'#EXTINF:-1, {clean_name}\n'
            # Hem VLC opsiyonu hem de link sonu header eklemesi (En uyumlu yöntem)
            m3u_output += f'#EXTVLCOPT:http-user-agent={user_agent}\n'
            m3u_output += f'#EXTVLCOPT:http-referrer={active_domain}/\n'
            m3u_output += f'{stream_url}|User-Agent={user_agent}&Referer={active_domain}/\n\n'

        # 4. Dosyayı Yaz
        with open("liste.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_output)
        
        print(f"Başarılı! {len(channel_ids)} kanal listeye eklendi.")

    except Exception as e:
        print(f"Hata oluştu: {str(e)}")

if __name__ == "__main__":
    generate_iptv_list()
