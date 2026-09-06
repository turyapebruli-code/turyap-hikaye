# Turyap Hikaye Otomasyonu

Google yorumlarindan uretilmis hikaye gorsellerini Instagram'da
(@turyap.ebruli) 4 saatte bir otomatik yayinlar.

## Nasil calisir

- `gorseller/` icindeki JPEG'ler sirayla paylasilir, liste bitince basa doner.
- `durum.json` sirayi tutar; her basarili paylasimdan sonra depoya geri yazilir.
- `.github/workflows/hikaye.yml` zamanlayici (UTC 01,05,09,13,17,21 =
  Turkiye saati 04:00, 08:00, 12:00, 16:00, 20:00, 00:00).
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
sirasi belirler (hikaye_41.jpg gibi).

## Elle calistirma

Actions sekmesi > "Instagram hikaye paylas" > "Run workflow".
