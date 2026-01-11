import requests
import re

# Tüm kanal listeniz
kanallar = [
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

def kalsayici():
    m3u_icerik = "#EXTM3U\n"
    # Site bazen domain değiştirdiği için burayı güncel tutun
    ana_domain = "https://birazcikspor44.xyz" 
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Referer': 'https://birazcikspor.com/'
    }

    for kanal in kanallar:
        try:
            target_url = f"{ana_domain}/event.html?id={kanal}"
            response = requests.get(target_url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                # Regex: Hem tek tırnak hem çift tırnak destekli
                # 'const baseurl = https://...' kısmını arar
                match = re.search(r'const\s+baseurl\s*=\s*["\'](https?://[^"\']+)["\']', response.text)
                
                if match:
                    base_url = match.group(1)
                    # checklist/ kısmını kanal_adi.m3u8 ile değiştiriyoruz
                    yayin_linki = base_url.replace('checklist/', f'{kanal}.m3u8')
                    m3u_icerik += f"#EXTINF:-1, {kanal}\n{yayin_linki}\n"
                    print(f"Eklendi: {kanal}")
                else:
                    print(f"Bulunamadı: {kanal} (Sayfa kaynağında baseurl yok)")
            else:
                print(f"Hata: {kanal} - Status Code: {response.status_code}")
                
        except Exception as e:
            print(f"Sistem Hatası: {kanal} -> {e}")

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_icerik)
    print("\n--- İşlem Tamamlandı. playlist.m3u oluşturuldu. ---")

if __name__ == "__main__":
    kalsayici()
