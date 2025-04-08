import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Wczytanie danych
df = pd.read_csv("curr_lct_dl.csv")

# Funkcja do wyodrębnienia lokalizacji z 'target'
def extract_location(target):
    try:
        parts = target.split('-vm-')
        if len(parts) > 1:
            return parts[1].split('.')[0]
        return None
    except:
        return None

# Przetwarzanie danych
df['location'] = df['target'].apply(extract_location)
df['dtime'] = pd.to_datetime(df['dtime'])

# 📈 Średnia dzienna prędkość (bytes/sec) dla wszystkich lokalizacji
time_series = df.groupby([pd.Grouper(key='dtime', freq='D'), 'location'])['bytes_sec'].mean().reset_index()

# Średnia prędkość na lokalizację
avg_bytes_sec = df.groupby('location')['bytes_sec'].mean().sort_values(ascending=False)

# Wykres 1 – Średnia dzienna prędkość
plt.figure(figsize=(14, 7))
sns.lineplot(data=time_series, x='dtime', y='bytes_sec', hue='location', marker='o')
plt.title("Średnia dzienna prędkość (bytes/sec) dla wszystkich lokalizacji")
plt.xlabel("Data")
plt.ylabel("Średnia prędkość (bytes/sec)")
plt.xticks(rotation=45)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# Wykres 2 – Top 5 lokalizacji wg średniej prędkości
top_5_by_speed = avg_bytes_sec.head(5)
plt.figure(figsize=(8, 5))
sns.barplot(x=top_5_by_speed.values, y=top_5_by_speed.index, palette="viridis")
plt.title("Top 5 lokalizacji wg średniej prędkości")
plt.xlabel("Średnia prędkość (bytes/sec)")
plt.ylabel("Lokalizacja")
plt.tight_layout()
plt.show()

# Wykres 3 – Średni czas trwania testów dla wszystkich lokalizacji
avg_duration = df.groupby('location')['duration'].mean()
plt.figure(figsize=(10, 6))
sns.barplot(x=avg_duration.values, y=avg_duration.index, palette="Oranges_d")
plt.title("Średni czas trwania testów (s) dla wszystkich lokalizacji")
plt.xlabel("Czas trwania (s)")
plt.ylabel("Lokalizacja")
plt.tight_layout()
plt.show()

# Wykres 4 – Liczba błędów na lokalizację
errors = df[df['error_code'] != 'NO_ERROR']
error_counts = errors['location'].value_counts()
plt.figure(figsize=(10, 6))
sns.barplot(x=error_counts.values, y=error_counts.index, palette="Reds_d")
plt.title("Liczba błędów na lokalizację (error_code ≠ NO_ERROR)")
plt.xlabel("Liczba błędów")
plt.ylabel("Lokalizacja")
plt.tight_layout()
plt.show()

# 🔍 Statystyki opisowe
print("📌 Statystyki opisowe dla 'bytes_sec' i 'duration':")
print(df[['bytes_sec', 'duration']].describe())

# 🔥 Korelacje
corr = df[['bytes_sec', 'duration', 'packets_sent', 'packets_received', 'bytes_total']].corr()
plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", square=True)
plt.title("Mapa korelacji dla zmiennych numerycznych")
plt.tight_layout()
plt.show()

# 📈 Rozkład – bytes_sec (dla wszystkich lokalizacji)
plt.figure(figsize=(12, 6))
sns.histplot(data=df, x="bytes_sec", hue="location", kde=True, bins=40, multiple="stack")
plt.title("Rozkład prędkości (bytes/sec) – wszystkie lokalizacje")
plt.xlabel("bytes/sec")
plt.ylabel("Liczba testów")
plt.tight_layout()
plt.show()

# 📉 Rozkład – duration (dla wszystkich lokalizacji)
plt.figure(figsize=(12, 6))
sns.histplot(data=df, x="duration", hue="location", kde=True, bins=40, multiple="stack")
plt.title("Rozkład czasu trwania testów – wszystkie lokalizacje")
plt.xlabel("Czas trwania (s)")
plt.ylabel("Liczba testów")
plt.tight_layout()
plt.show()
