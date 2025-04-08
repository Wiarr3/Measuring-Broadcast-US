import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Upewnijmy się, że kolumna z lokalizacją jest dodana
df = pd.read_csv("curr_lct_dl.csv")
def extract_location(target):
    try:
        parts = target.split('-vm-')
        if len(parts) > 1:
            return parts[1].split('.')[0]
        return None
    except:
        return None

df['location'] = df['target'].apply(extract_location)

# Grupowanie danych po lokalizacji
location_counts = df['location'].value_counts()

# Średnia prędkość bajtów na sekundę na lokalizację
avg_bytes_sec = df.groupby('location')['bytes_sec'].mean().sort_values(ascending=False)

# Średni czas trwania testów na lokalizację
avg_duration = df.groupby('location')['duration'].mean().sort_values(ascending=False)

# Liczba błędów (różnych niż NO_ERROR) na lokalizację
errors_per_location = df[df['error_code'] != 'NO_ERROR'].groupby('location').size()

# Tworzenie wykresów
plt.figure(figsize=(16, 12))

# Wykres 1 – Liczba testów
plt.subplot(2, 2, 1)
sns.barplot(x=location_counts.values, y=location_counts.index, palette="Blues_d")
plt.title("Liczba testów na lokalizację")
plt.xlabel("Liczba testów")
plt.ylabel("Lokalizacja")

# Wykres 2 – Średnia prędkość
plt.subplot(2, 2, 2)
sns.barplot(x=avg_bytes_sec.values, y=avg_bytes_sec.index, palette="Greens_d")
plt.title("Średnia prędkość (bytes/sec) na lokalizację")
plt.xlabel("Średnia prędkość")
plt.ylabel("Lokalizacja")

# Wykres 3 – Średni czas trwania testu
plt.subplot(2, 2, 3)
sns.barplot(x=avg_duration.values, y=avg_duration.index, palette="Oranges_d")
plt.title("Średni czas trwania testu (s) na lokalizację")
plt.xlabel("Czas trwania (s)")
plt.ylabel("Lokalizacja")

# Wykres 4 – Liczba błędów
plt.subplot(2, 2, 4)
sns.barplot(x=errors_per_location.values, y=errors_per_location.index, palette="Reds_d")
plt.title("Liczba błędów na lokalizację")
plt.xlabel("Liczba błędów")
plt.ylabel("Lokalizacja")

plt.tight_layout()
plt.show()
