import pandas as pd

# JSON dosyasını oku
data = pd.read_json("mydatabase.cars.json")  # Dosya adını değiştirin

# Veriyi CSV dosyasına yaz
data.to_csv("data.csv", index=False)  # Dosya adını değiştirin

import json
import csv

# JSON dosyasını oku
with open("mydatabase.cars.json", "r") as f:
    data = json.load(f)

# CSV dosyasını aç
with open("data.csv", "w", newline="") as f:
    writer = csv.writer(f)

    # Başlıkları yaz
    writer.writerow(data[0].keys())  # İlk öğenin anahtarlarını kullan

    # Verileri satır satır yaz
    for item in data:
        writer.writerow(item.values())  # Her öğenin değerlerini listeye dönüştür

# Dosyaları kapat (açık kalmalarına gerek yok)
