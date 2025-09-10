# duplicateDataCleaner

CSV dosyalarındaki tekrar eden (duplicate) kayıtları akıllıca temizleyen basit bir Python aracı.

Bu araç, belirttiğiniz metin sütunundaki ilk 20 kelime ve kullanıcı adı sütununu birlikte değerlendirerek aynı içeriğin kopyalarını bulur. Her duplicate grup içinde en uzun metne sahip kayıt korunur, diğerleri kaldırılır.

## Özellikler
- İlk 20 kelime + kullanıcı adı kombinasyonu ile grup bazlı duplicate tespiti
- Her grupta en uzun metinli kaydı otomatik seçme
- Orijinal dosyanın üzerine yazma veya farklı bir çıktı dosyasına kaydetme
- Sütun adları ve dosya yolu parametreleri ile esnek kullanım

## Gereksinimler
- Python 3.8+
- pandas

Kurulum için:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Alternatif olarak:

```bash
pip install pandas
```

## Kullanım
`cleaner.py` içindeki `clean_csv_duplicates` fonksiyonunu doğrudan kullanabilir veya dosyanın en altındaki örnek çalıştırmayı kendi değerlerinizle düzenleyip çalıştırabilirsiniz.

### Örnek (Komut Satırından Çalıştırma)
`cleaner.py` içerisindeki değişkenleri düzenleyin:
- `csv_dosya_yolu`: Girdi CSV dosyanızın yolu
- `metin_sutunu`: İlk 20 kelimesi kontrol edilecek sütun adı (ör. `text_original`)
- `kullanici_sutunu`: Kullanıcı adı sütun adı (ör. `author_name`)
- `output_file`: Çıktı dosyası adı (örn. `temizlenmisDosya.csv`)

Ardından çalıştırın:

```bash
python cleaner.py
```

### Örnek (Kod İçinden Kullanım)

```python
from cleaner import clean_csv_duplicates

cleaned_df = clean_csv_duplicates(
    csv_file_path="istanbulAirport.csv",
    text_column="text_original",
    username_column="author_name",
    output_file="temizlenmisDosya.csv",
)
```

## Parametreler
- `csv_file_path` (str): Girdi CSV dosyasının yolu.
- `text_column` (str, varsayılan: `b`): İlk 20 kelimesi alınacak metin sütunu.
- `username_column` (str, varsayılan: `d`): Kullanıcı adı sütunu.
- `output_file` (str | None): Çıktı dosyası yolu. Boş bırakılırsa orijinal dosyanın üzerine yazar.

## Nasıl Çalışır?
1. CSV dosyası okunur ve ilgili sütunların varlığı kontrol edilir.
2. Metin sütunundan sadece harf ve rakamlar kalacak şekilde ilk 20 kelime çıkarılır.
3. Kullanıcı adları küçük harfe çevrilip boşluklardan arındırılır.
4. Aynı (ilk 20 kelime, kullanıcı) çiftine sahip kayıtlar grup yapılır.
5. Her grup için en uzun metinli kayıt seçilir ve diğerleri kaldırılır.
6. Sonuçlar belirtilen dosyaya yazılır.

## Önemli Notlar ve İpuçları
- Kod, UTF-8 kodlaması ile okur/yazar. Dosyanız farklı kodlamadaysa `read_csv`/`to_csv` parametrelerini uyarlayın.
- `text_column` ve `username_column` adlarının girdi dosyanızdaki sütun isimleriyle birebir eşleştiğinden emin olun.
- Çok büyük dosyalar için bellek kullanımı artabilir. Gerekirse parça parça işleme ya da daha gelişmiş stratejiler planlanabilir.

## Geliştirme
- Test CSV dosyalarıyla farklı senaryoları deneyin (eksik sütun, boş değerler, çok uzun metinler vb.).
- İhtiyaca göre ilk 20 kelime kuralını parametreleştirmek veya benzerlik tabanlı tespit eklemek mümkündür.

## Lisans
Bu proje MIT lisansı ile lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.
