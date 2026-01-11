import requests
import re

# Kanal isimleri ve ID eşleşmeleri
kanal_verileri = [
    ("beIN Sport 1 HD", "androstreamlivebiraz1"),
    ("beIN Sport 1 HD", "androstreamlivebs1"),
    ("beIN Sport 2 HD", "androstreamlivebs2"),
    ("beIN Sport 3 HD", "androstreamlivebs3"),
    ("beIN Sport 4 HD", "androstreamlivebs4"),
    ("beIN Sport 5 HD", "androstreamlivebs5"),
    ("beIN Sport Max 1 HD", "androstreamlivebsm1"),
    ("beIN Sport Max 2 HD", "androstreamlivebsm2"),
    ("S Sport 1 HD", "androstreamlivess1"),
    ("S Sport 2 HD", "androstreamlivess2"),
    ("Tivibu Sport HD", "androstreamlivets"),
    ("Tivibu Sport 1 HD", "androstreamlivets1"),
    ("Tivibu Sport 2 HD", "androstreamlivets2"),
    ("Tivibu Sport 3 HD", "androstreamlivets3"),
    ("Tivibu Sport 4 HD", "androstreamlivets4"),
    ("Smart Sport 1 HD", "androstreamlivesm1"),
    ("Smart Sport 2 HD", "androstreamlivesm2"),
    ("Euro Sport 1 HD", "androstreamlivees1"),
    ("Euro Sport 2 HD", "androstreamlivees2"),
    ("Tabii HD", "androstreamlivetb"),
    ("Tabii 1 HD", "androstreamlivetb1"),
    ("Tabii 2 HD", "androstreamlivetb2"),
    ("Tabii 3 HD", "androstreamlivetb3"),
    ("Tabii 4 HD", "androstreamlivetb4"),
    ("Tabii 5 HD", "androstreamlivetb5"),
    ("Tabii 6 HD", "androstreamlivetb6"),
    ("Tabii 7 HD", "androstreamlivetb7"),
    ("Tabii 8 HD", "androstreamlivetb8"),
    ("Exxen HD", "androstreamliveexn"),
    ("Exxen 1 HD", "androstreamliveexn1"),
    ("Exxen 2 HD", "androstreamliveexn2"),
    ("Exxen 3 HD", "androstreamliveexn3"),
    ("Exxen 4 HD", "androstreamliveexn4"),
    ("Exxen 5 HD", "androstreamliveexn5"),
    ("Exxen 6 HD", "androstreamliveexn6"),
    ("Exxen 7 HD", "androstreamliveexn7"),
    ("Exxen 8 HD", "androstreamliveexn8")
]

def kalsayici():
    m3u_icerik = "#EXTM3U\n"
    # Aktif domaini buradan kontrol edin
    ana_domain = "https://birazcikspor44.xyz" 
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://birazcikspor.com/',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    print("İşlem başlıyor...")

    for kanal_adi, kanal_id in kanal_verileri:
        try:
            target_url = f"{ana_domain}/event.html?id={kanal_id}"
            response = requests.get(target_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                # Regex ile baseurl çekme
                match = re.search(r'const\s+baseurl\s*=\s*["\'](https?://[^"\']+)["\']', response.text)
                
                if match:
                    base_url = match.group(1)
                    # 'checklist/' kısmını 'kanal_id.m3u8' ile değiştiriyoruz
                    yayin_url = base_url.replace('checklist/', f'{kanal_id}.m3u8')
                    
                    m3u_icerik += f'#EXTINF:-1 tvg-name="{kanal_adi}" group-title="Spor", {kanal_adi}\n'
                    m3u_icerik += f"{yayin_url}\n"
                    print(f"BAŞARILI: {kanal_adi}")
                else:
                    print(f"UYARI: {kanal_adi} için kaynak kodunda link bulunamadı.")
            else:
                print(f"HATA: {kanal_adi} (Durum Kodu: {response.status_code})")
                
        except Exception as e:
            print(f"SİSTEM HATASI: {kanal_adi} -> {str(e)}")

    # Dosyayı kaydet
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_icerik)
    
    print("\n--- Bitti! playlist.m3u dosyası güncellendi. ---")

if __name__ == "__main__":
    kalsayici()
