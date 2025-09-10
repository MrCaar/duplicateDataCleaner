import pandas as pd
import re

def get_first_20_words(text):
    """Metinden ilk 20 kelimeyi al"""
    if pd.isna(text):
        return ""
    
    # Sadece harf ve rakamları al, noktalama işaretlerini kaldır
    words = re.findall(r'\b\w+\b', str(text).lower())
    return ' '.join(words[:20])

def clean_csv_duplicates(csv_file_path, text_column='b', username_column='d', output_file=None):
    """
    CSV dosyasındaki duplicate kayıtları temizle
    
    Parameters:
    - csv_file_path: istanbulAirport.csv
    - text_column: İlk 20 kelimesini kontrol edilecek sütun adı (varsayılan: 'b')
    - username_column: Kullanıcı adı sütunu adı (varsayılan: 'd')
    - output_file: Çıktı dosyasının yolu (belirtilmezse orijinal dosya üzerine yazar)
    """
    
    try:
        # CSV dosyasını oku
        df = pd.read_csv(csv_file_path, encoding='utf-8')
        print(f"Orijinal kayıt sayısı: {len(df)}")
        print(f"Mevcut sütunlar: {list(df.columns)}")
        
        # Gerekli sütunların var olup olmadığını kontrol et
        if text_column not in df.columns:
            print(f"Hata: '{text_column}' sütunu bulunamadı!")
            print(f"Mevcut sütunlar: {list(df.columns)}")
            return
        
        if username_column not in df.columns:
            print(f"Hata: '{username_column}' sütunu bulunamadı!")
            print(f"Mevcut sütunlar: {list(df.columns)}")
            return
        
        # İlk 20 kelimeyi çıkar
        df['first_20_words'] = df[text_column].apply(get_first_20_words)
        
        # Kullanıcı adını normalize et
        df['normalized_username'] = df[username_column].astype(str).str.lower().str.strip()
        
        # Metin uzunluğunu hesapla
        df['text_length'] = df[text_column].astype(str).str.len()
        
        # Duplicate grupları bul
        duplicate_groups = df.groupby(['first_20_words', 'normalized_username'])
        
        # Her gruptan en uzun metne sahip olanı tut
        indices_to_keep = []
        removed_count = 0
        
        for name, group in duplicate_groups:
            if len(group) > 1:
                # Aynı grup içinde en uzun metne sahip kaydı bul
                max_length_idx = group['text_length'].idxmax()
                indices_to_keep.append(max_length_idx)
                removed_count += len(group) - 1
                print(f"Duplicate grup bulundu - Kullanıcı: '{name[1]}', İlk 20 kelime: '{name[0][:50]}...', {len(group)} kayıttan 1'i tutuldu")
            else:
                indices_to_keep.extend(group.index.tolist())
        
        # Temizlenmiş DataFrame oluştur
        cleaned_df = df.loc[indices_to_keep].copy()
        
        # Geçici sütunları kaldır
        cleaned_df = cleaned_df.drop(['first_20_words', 'normalized_username', 'text_length'], axis=1)
        
        # Sonucu kaydet
        output_path = output_file if output_file else csv_file_path
        cleaned_df.to_csv(output_path, index=False, encoding='utf-8')
        
        print(f"\nTemizleme tamamlandı!")
        print(f"Kaldırılan duplicate kayıt sayısı: {removed_count}")
        print(f"Kalan kayıt sayısı: {len(cleaned_df)}")
        print(f"Sonuç dosyası: {output_path}")
        
        return cleaned_df
        
    except Exception as e:
        print(f"Hata oluştu: {str(e)}")
        return None

# Kullanım örneği
if __name__ == "__main__":
    # Dosya yolunu ve sütun adlarını buradan değiştirebilirsiniz
    csv_dosya_yolu = "istanbulAirport.csv"  # CSV dosyanızın yolunu buraya yazın
    metin_sutunu = "text_original"    # İlk 20 kelimesini kontrol edilecek sütun
    kullanici_sutunu = "author_name"  # Kullanıcı adı sütunu

    # Temizleme işlemini çalıştır
    result = clean_csv_duplicates(
        csv_file_path=csv_dosya_yolu,
        text_column=metin_sutunu,
        username_column=kullanici_sutunu,
        output_file="temizlenmisDosya.csv"  # İsterseniz farklı bir dosya adı verebilirsiniz
    )