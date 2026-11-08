# Turyap Hikaye Otomasyonu

Google yorumlarindan uretilmis hikaye gorsellerini Instagram'da
(@turyap.ebruli) 7 saatte bir otomatik yayinlar.

## Nasil calisir

- `gorseller/` icindeki JPEG'ler sirayla paylasilir, liste bitince basa doner.
- `durum.json` sirayi tutar; her basarili paylasimdan sonra depoya geri yazilir.
- `.github/workflows/hikaye.yml` her saat uyanir; `paylas.py` son paylasimdan
  7 saat gecmediyse paylasmadan cikar (`ARALIK_SAAT` ile degistirilir).
- Paylasim basarisiz olursa is HATA ile biter ve GitHub otomatik e-posta atar.

## Gerekli ayarlar (Settings > Secrets and variables > Actions)

| Secret | Deger |
|---|---|
| `IG_KULLANICI_ID` | 17841435008101782 |
| `ERISIM_ANAHTARI` | Meta Sayfa erisim anahtari (suresiz) |

## Depo herkese acik olmali

Instagram gorseli `raw.githubusercontent.com` uzerinden kendisi indiriyor.
Depo gizli olursa Instagram gorsele erisemez ve paylasim basarisiz olur.
Buradaki gorseller zaten herkese acik Google yorumlarindan uretilmistir.

## Yeni yorum eklemek

Yeni hikaye gorsellerini `gorseller/` klasorune ekleyin, isimlendirme
sirasi belirler (hikaye_110.jpg gibi). Gorseller ../turyap-hikaye/hikaye_uret_v2.py ile uretilir..

## Elle calistirma

Actions sekmesi > "Instagram hikaye paylas" > "Run workflow".
Elle calistirma 7 saati beklemeden hemen paylasir.
