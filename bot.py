import requests
import re

# Senin verdiğin kanal listesi
kanallar = [
    "androstreamlivebiraz1", "androstreamlivebs1", "androstreamlivebs2",
    # ... diğer tüm kanalları buraya eklediğini varsayıyoruz
]

def kalsayici():
    m3u_icerik = "#EXTM3U\n"
    # 1. Adım: Ana domaini belirle (Yönlendirmeleri takip et)
    ana_url = "https://birazcikspor44.xyz" # Dinamik olarak çekilebilir
    
    for kanal in kanallar:
        try:
            target_url = f"{ana_url}/event.html?id={kanal}"
            response = requests.get(target_url, timeout=10)
            
            # 2. Adım: Kaynak kodun içindeki baseurl'i yakala
            # Regex ile 'const baseurl = https://.../' yapısını arıyoruz
            match = re.search(r'const baseurl = (https?://[^\s\'"]+)', response.text)
            
            if match:
                yayin_linki = match.group(1).replace('checklist/', f'{kanal}.m3u8')
                m3u_icerik += f"#EXTINF:-1,{kanal}\n{yayin_linki}\n"
                print(f"Başarılı: {kanal}")
        except Exception as e:
            print(f"Hata: {kanal} çekilemedi. {e}")

    # 3. Adım: Dosyaya yaz
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_icerik)

if __name__ == "__main__":
    kalsayici()
