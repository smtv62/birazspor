import requests
import re
import os

def generate_iptv_list():
    # TV versiyonları için daha uyumlu User-Agent
    user_agent = "IPTVSmarters/3.0 (Android; 10; TV)"
    
    headers = {
        'User-Agent': user_agent,
        'Referer': 'https://birazcikspor.com/'
    }

    # Kanal ID'leri ve Gerçek İsimleri Eşleştirme
    channels = [
        ("androstreamlivebiraz1", "BeIN Sports 1"),
        ("androstreamlivebs1", "BeIN Sports 1"),
        ("androstreamlivebs2", "BeIN Sports 2"),
        ("androstreamlivebs3", "BeIN Sports 3"),
        ("androstreamlivebs4", "BeIN Sports 4"),
        ("androstreamlivebs5", "BeIN Sports 5"),
        ("androstreamlivebsm1", "BeIN Sports Max 1"),
        ("androstreamlivebsm2", "BeIN Sports Max 2"),
        ("androstreamlivess1", "S Sport"),
        ("androstreamlivess2", "S Sport 2"),
        ("androstreamliveplus", "S Sport Plus"),
        ("androstreamlivets", "Tivibu Spor"),
        ("androstreamlivets1", "Tivibu Spor 1"),
        ("androstreamlivets2", "Tivibu Spor 2"),
        ("androstreamlivets3", "Tivibu Spor 3"),
        ("androstreamlivets4", "Tivibu Spor 4"),
        ("androstreamlivesm1", "Smart Spor 1"),
        ("androstreamlivesm2", "Smart Spor 2"),
        ("androstreamlivees1", "Euro Sport 1"),
        ("androstreamlivees2", "Euro Sport 2"),
        ("androstreamliveidman", "iDMAN Tv"),
        ("androstreamlivetrt1", "Trt 1"),
        ("androstreamlivetrtspor", "Trt Spor"),
        ("androstreamlivetrtsporyildiz", "Trt Spor Yildiz"),
        ("androstreamliveatv", "Atv"),
        ("androstreamliveaspor", "A Spor"),
        ("androstreamlivea2", "A2"),
        ("androstreamlivetjk", "Tjk Tv"),
        ("androstreamlivehtspor", "Ht Spor"),
        ("androstreamlivenba", "Nba Tv"),
        ("androstreamlivetv8", "Tv8"),
        ("androstreamlivetv85", "Tv8,5"),
        ("androstreamlivetb", "Tabi Spor"),
        ("androstreamlivetb1", "Tabi Spor 1"),
        ("androstreamlivetb2", "Tabi Spor 2"),
        ("androstreamlivetb3", "Tabi Spor 3"),
        ("androstreamlivetb4", "Tabi Spor 4"),
        ("androstreamlivetb5", "Tabi Spor 5"),
        ("androstreamlivetb6", "Tabi Spor 6"),
        ("androstreamlivetb7", "Tabi Spor 7"),
        ("androstreamlivetb8", "Tabi Spor 8"),
        ("androstreamlivefbtv", "Fb Tv"),
        ("androstreamlivecbc", "Cbc Sport"),
        ("androstreamlivegstv", "Gs Tv"),
        ("androstreamlivesportstv", "Sports Tv"),
        ("androstreamliveexn", "Exxen Tv"),
        ("androstreamliveexn1", "Exxen Sports 1"),
        ("androstreamliveexn2", "Exxen Sports 2"),
        ("androstreamliveexn3", "Exxen Sports 3"),
        ("androstreamliveexn4", "Exxen Sports 4"),
        ("androstreamliveexn5", "Exxen Sports 5"),
        ("androstreamliveexn6", "Exxen Sports 6"),
        ("androstreamliveexn7", "Exxen Sports 7"),
        ("androstreamliveexn8", "Exxen Sports 8")
    ]

    try:
        # 1. Aktif Domaini Bul
        print("Site taranıyor...")
        main_res = requests.get("https://birazcikspor.com", headers=headers, timeout=15)
        active_site_match = re.search(r'href="(https?://birazcikspor[^"]+\.xyz)"', main_res.text)
        active_domain = active_site_match.group(1).rstrip('/') if active_site_match else "https://birazcikspor44.xyz"
        print(f"Hedef Site: {active_domain}")

        # 2. BaseURL'yi Çek
        sample_url = f"{active_domain}/event.html?id=androstreamlivebiraz1"
        sample_res = requests.get(sample_url, headers=headers, timeout=15).text
        base_urls = re.findall(r'["\'](https?://[^"\']+/checklist/)["\']', sample_res)
        
        if not base_urls:
            print("HATA: BaseURL bulunamadı!")
            return
        
        final_base = base_urls[0]
        print(f"Kaynak URL: {final_base}")

        # 3. M3U İçeriğini Oluştur
        m3u_output = "#EXTM3U\n"
        
        for cid, cname in channels:
            stream_url = f"{final_base}{cid}.m3u8"
            
            # Televizo TV ve ExoPlayer için genişletilmiş header tanımları
            m3u_output += f'#EXTINF:-1 tvg-name="{cname}", {cname}\n'
            m3u_output += f'#EXTHTTP:{{"User-Agent":"{user_agent}","Referer":"{active_domain}/"}}\n'
            m3u_output += f'#EXTVLCOPT:http-user-agent={user_agent}\n'
            m3u_output += f'#EXTVLCOPT:http-referrer={active_domain}/\n'
            m3u_output += f'{stream_url}|User-Agent={user_agent}&Referer={active_domain}/\n\n'

        # 4. Dosyayı Yaz
        with open("liste.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_output)
        
        print(f"Başarılı! {len(channels)} kanal listeye eklendi.")

    except Exception as e:
        print(f"Hata oluştu: {str(e)}")

if __name__ == "__main__":
    generate_iptv_list()
