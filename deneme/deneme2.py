import pandas as pd

# JSON dosyasını oku
data = pd.read_json("dataconverter.cars.json")  # Dosya adını değiştirin

# Veriyi CSV dosyasına yaz
data.to_csv("data2.csv", index=False)  # Dosya adını değiştirin

import json
import csv

# JSON dosyasını oku
with open("dataconverter.cars.json", "r") as f:
    data = json.load(f)

# CSV dosyasını aç
with open("data2.csv", "w", newline="") as f:
    writer = csv.writer(f)

    # Başlıkları yaz
    writer.writerow(data[0].keys())  # İlk öğenin anahtarlarını kullan

    # Verileri satır satır yaz
    for item in data:
        writer.writerow(item.values())  # Her öğenin değerlerini listeye dönüştür

# Dosyaları kapat (açık kalmalarına gerek yok)
