import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# CSV dosyasını oku
df = pd.read_csv('data.csv')
df['Fiyat'] = df['Fiyat'].astype(float)
df.dropna(axis=0, inplace=True)
print(df.isnull().sum())

outlier_threshold = 1

# Yeni bir DataFrame oluşturarak temizlenmiş veriyi saklayacağız
cleaned_df = pd.DataFrame(columns=df.columns)

# Her bir "Model" grubu için aykırı değerleri tespit edip silme işlemi
for model_value, group in df.groupby('Model'):
    # 'Fiyat' sütunundaki aykırı değerlerin indekslerini bul
    Q1 = group['Fiyat'].quantile(0.25)
    Q3 = group['Fiyat'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - outlier_threshold * IQR
    upper_bound = Q3 + outlier_threshold * IQR
    outlier_indices = group[(group['Fiyat'] < lower_bound) | (group['Fiyat'] > upper_bound)].index

    # Aykırı değerleri sil
    group.drop(outlier_indices, inplace=True)

    # Temizlenmiş veriyi ana DataFrame'e ekle
    cleaned_df = pd.concat([cleaned_df, group], ignore_index=True)

# Normalleştirme için Min-Max Scaler'ı kullan
scaler = MinMaxScaler(feature_range=(0, 1))
normalized_values = scaler.fit_transform(cleaned_df[['Fiyat']])
cleaned_df['Fiyat'] = normalized_values.flatten()

# Temizlenmiş veriyi CSV olarak kaydet
cleaned_df.to_csv('temizlenmis_veri.csv', index=False)