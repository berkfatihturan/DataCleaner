import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import pymongo

import config
from src.DataFinder import DataFinder

# MongoDB bağlantısı
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["cars_copy"]

# Veritabanından verileri çekme
data_list = list(collection.find({}, {"_id": 0}).sort({"name": 1}))  # "_id" sütununu almıyoruz

dataFinder = DataFinder()
field_configs = dataFinder.get_data_from_json(file_path=config.FIELD_CONFIG_PATH)
if field_configs is not None:
    # Check each field in the label mapping file
    for data in data_list:
        for field_name in field_configs.keys():
            if not field_name in data and field_configs[field_name]["operation"] != "DELETE":
                data[field_name] = 0

for data in data_list:
    print(data)
    print("-----------")
# Verileri numpy dizisine dönüştürme ve Fiyat sütununu çıkartma
X = np.array([list(data.values())[:-1] for data in data_list], dtype=float)  # Verileri float tipine dönüştürme
y = np.array([data["Fiyat"] for data in data_list], dtype=float)  # Fiyatları float tipine dönüştürme

# Verileri normalize etme
scaler = MinMaxScaler()
X_normalized = scaler.fit_transform(X)

# Eğitim ve test veri setlerini oluşturma
X_train, X_test, y_train, y_test = train_test_split(X_normalized, y, test_size=0.2, random_state=42)

# Yatay Sinir Ağı Modeli Oluşturma
model = Sequential()
model.add(Dense(64, input_dim=X_train.shape[1], activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='linear'))

# Modeli Derleme
model.compile(optimizer='adam', loss='mean_squared_error')

# Modeli Eğitme
model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2, verbose=1)

# Modeli Değerlendirme
# loss = model.evaluate(X_test, y_test, verbose=0)
# print(f"Test Kaybı: {loss}")

# Tahmin Yapma
sample_data = X_test[0].reshape(1, -1)  # Örnek bir veri
predicted_price = model.predict(sample_data)[0][0]
print("Tahmin Edilen Fiyat:", predicted_price)
