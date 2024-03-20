import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('temizlenmis_veri.csv')


# Grafiği çiz
# plt.plot(df["Fiyat"], df["Model"])
plt.bar(df["Model"],df["Fiyat"])


# Grafiği göster
plt.show()