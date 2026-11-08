# -*- coding: utf-8 -*-
"""Sıradaki hikâyeyi Instagram'da yayınlar.

GitHub Actions her saat çalıştırır; son paylaşımdan 7 saat geçtiyse paylaşır. Hangi görselin sırada olduğunu
durum.json tutar; paylaşım başarılı olursa sıra bir ilerler ve depoya
geri yazılır. Liste bitince başa döner.

Gerekli ortam değişkenleri (GitHub Secrets):
  IG_KULLANICI_ID  - Instagram işletme hesabı kimliği
  ERISIM_ANAHTARI  - Süresiz Sayfa erişim anahtarı
"""
import calendar
import json
import os
import sys
import time
import urllib.parse
import urllib.request

SURUM = "v23.0"
GORSEL_KLASOR = "gorseller"
DURUM_DOSYA = "durum.json"
ARALIK_SAAT = 7          # iki hikâye arası (kullanıcı kararı, 8 Kasım 2026)
TOLERANS_SAAT = 0.25     # Actions zamanlayıcısı birkaç dakika kayabiliyor


def cik(mesaj):
    """Hata mesajını yaz ve başarısız çık — Actions e-posta göndersin."""
    print(f"HATA: {mesaj}", file=sys.stderr)
    sys.exit(1)


def istek(yol, veri=None):
    url = f"https://graph.facebook.com/{SURUM}/{yol}"
    govde = urllib.parse.urlencode(veri).encode() if veri else None
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=govde), timeout=60) as c:
            return json.loads(c.read().decode())
    except urllib.error.HTTPError as e:
        detay = e.read().decode()[:400]
        cik(f"Graph API {e.code} — {detay}")
    except Exception as e:  # ağ hatası vb.
        cik(f"İstek başarısız: {e}")


def gorselleri_bul():
    if not os.path.isdir(GORSEL_KLASOR):
        cik(f"'{GORSEL_KLASOR}' klasörü yok")
    d = sorted(a for a in os.listdir(GORSEL_KLASOR)
               if a.lower().endswith((".jpg", ".jpeg", ".png")))
    if not d:
        cik("Paylaşılacak görsel yok")
    return d


def durumu_oku(toplam):
    try:
        with open(DURUM_DOSYA, encoding="utf-8") as f:
            return int(json.load(f).get("sira", 0)) % toplam
    except (OSError, ValueError, json.JSONDecodeError):
        return 0


def son_paylasimdan_beri_saat():
    """Son başarılı paylaşımdan bu yana geçen saat; bilinmiyorsa None."""
    try:
        with open(DURUM_DOSYA, encoding="utf-8") as f:
            z = json.load(f).get("son_zaman", "")
        t = calendar.timegm(time.strptime(z, "%Y-%m-%d %H:%M:%S UTC"))
    except (OSError, ValueError, json.JSONDecodeError):
        return None
    return (time.time() - t) / 3600


def durumu_yaz(sira, dosya):
    with open(DURUM_DOSYA, "w", encoding="utf-8") as f:
        json.dump({"sira": sira,
                   "son_paylasilan": dosya,
                   "son_zaman": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())},
                  f, ensure_ascii=False, indent=2)


def main():
    ig = os.environ.get("IG_KULLANICI_ID", "").strip()
    anahtar = os.environ.get("ERISIM_ANAHTARI", "").strip()
    depo = os.environ.get("GITHUB_REPOSITORY", "").strip()
    dal = os.environ.get("GITHUB_REF_NAME", "main").strip()

    if not ig or not anahtar:
        cik("IG_KULLANICI_ID veya ERISIM_ANAHTARI tanımlı değil (GitHub Secrets)")
    if not depo:
        cik("GITHUB_REPOSITORY yok — bu script GitHub Actions içinde çalışmalı")

    # Zamanlayıcı her saat uyanır; son paylaşımdan ARALIK_SAAT geçmediyse çıkar.
    # Elle çalıştırmada (ZORLA=1) beklemeden paylaşır.
    gecen = son_paylasimdan_beri_saat()
    if os.environ.get("ZORLA") != "1" and gecen is not None and gecen < ARALIK_SAAT - TOLERANS_SAAT:
        print(f"Son paylaşımdan bu yana {gecen:.1f} saat geçti; "
              f"{ARALIK_SAAT} saat dolmadı, bu tur paylaşım yok.")
        return

    gorseller = gorselleri_bul()
    sira = durumu_oku(len(gorseller))
    dosya = gorseller[sira]
    gorsel_url = f"https://raw.githubusercontent.com/{depo}/{dal}/{GORSEL_KLASOR}/{urllib.parse.quote(dosya)}"

    print(f"Sıra {sira + 1}/{len(gorseller)} — {dosya}")
    print(f"Görsel: {gorsel_url}")

    # 1) Medya kabı oluştur
    kap = istek(f"{ig}/media", {
        "image_url": gorsel_url,
        "media_type": "STORIES",
        "access_token": anahtar,
    })
    kap_id = kap.get("id")
    if not kap_id:
        cik(f"Medya kabı oluşmadı: {kap}")
    print(f"Medya kabı: {kap_id}")

    # 2) Instagram görseli indirene kadar bekle
    for deneme in range(12):
        time.sleep(5)
        d = istek(f"{kap_id}?fields=status_code,status&access_token={anahtar}")
        durum = d.get("status_code")
        if durum == "FINISHED":
            break
        if durum == "ERROR":
            cik(f"Instagram görseli işleyemedi: {d.get('status')}")
        print(f"  hazırlanıyor... ({durum})")
    else:
        cik("Medya 60 saniyede hazır olmadı")

    # 3) Yayınla
    sonuc = istek(f"{ig}/media_publish", {
        "creation_id": kap_id,
        "access_token": anahtar,
    })
    if not sonuc.get("id"):
        cik(f"Yayınlanamadı: {sonuc}")

    print(f"YAYINLANDI — hikaye kimligi {sonuc['id']}")
    durumu_yaz((sira + 1) % len(gorseller), dosya)


if __name__ == "__main__":
    main()
