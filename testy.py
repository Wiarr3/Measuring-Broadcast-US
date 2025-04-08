import pandas as pd
import plotly.express as px

# Wczytanie danych
df = pd.read_csv("curr_lct_dl.csv")  # Zmień na ścieżkę do swojego pliku

# Funkcja do wyodrębniania lokalizacji z 'target'
def extract_location(target):
    try:
        parts = target.split('-vm-')
        if len(parts) > 1:
            return parts[1].split('.')[0]
        return None
    except:
        return None

# Dodanie kolumny z lokalizacją
df['location'] = df['target'].apply(extract_location)

# Unikalne lokalizacje
unique_locations = df['location'].dropna().unique()
print("Unikalne lokalizacje:", sorted(unique_locations))  # Wyświetlenie lokalizacji

# Ręcznie przypisane współrzędne dla lokalizacji (dodaj więcej lokalizacji jeśli chcesz)
location_coords = {
    'ashburn-us': {'lat': 39.0403, 'lon': -77.4852},
    'atlanta-us': {'lat': 33.7537, 'lon': -84.3863},
    'chicgao-us': {'lat': 41.8818, 'lon': -87.6232},
    'dallas-us': {'lat': 32.7792, 'lon': -96.8089},
    'denver-us': {'lat': 39.7421, 'lon': -104.9915},
    'losangeles-us': {'lat': 34.0522, 'lon': -118.2437},
    'miami-us': {'lat': 25.7617, 'lon': -80.1918},
    'newyork-us': {'lat': 40.7306, 'lon': -73.9352},
    'sanjose-us': {'lat': 37.3355, 'lon': -121.8931},
    'seattle-us': {'lat': 47.6081, 'lon': -122.3352},
}

# Tworzenie DataFrame z metrykami (np. średnia prędkość i liczba testów)
metrics = df.groupby('location').agg({
    'bytes_sec': 'mean',
    'duration': 'mean',
    'target': 'count'
}).rename(columns={'target': 'test_count'}).reset_index()

# Dodajemy współrzędne do lokalizacji
metrics['lat'] = metrics['location'].map(lambda loc: location_coords.get(loc, {}).get('lat'))
metrics['lon'] = metrics['location'].map(lambda loc: location_coords.get(loc, {}).get('lon'))

# Usuwamy lokalizacje, które nie mają przypisanych współrzędnych
metrics = metrics.dropna(subset=['lat', 'lon'])

# Usuwamy wiersze z NaN w kolumnie 'bytes_sec' (usuwanie lub zastępowanie NaN)
metrics = metrics.dropna(subset=['bytes_sec'])  # Alternatywnie: 'metrics['bytes_sec'] = metrics['bytes_sec'].fillna(0)'

# Dodanie liczby błędów (przykład, jeśli chcesz analizować błędy)
metrics['error_count'] = df.groupby('location')['error_code'].apply(lambda x: (x != 'NO_ERROR').sum()).reset_index(drop=True)

# Tworzymy mapkę z Plotly
fig = px.scatter_geo(metrics,
    lat='lat',
    lon='lon',
    text=metrics['location'],  # Przekazujemy tylko listę z lokalizacjami jako tekst
    size='bytes_sec',  # Możesz zmienić na inną metrykę
    color='bytes_sec',  # Możesz zmienić na inną metrykę
    hover_name='location',
    hover_data={'bytes_sec': True, 'duration': True, 'test_count': True, 'lat': False, 'lon': False, 'error_count': True},
    color_continuous_scale='Viridis',
    projection='orthographic',  # Możesz zmienić na inną projekcję, np. 'natural earth', 'mercator', 'equirectangular'
    title="🌍 Średnia prędkość (bytes/sec) dla lokalizacji",
)

# Dodatkowe opcje
fig.update_layout(
    geo=dict(
        showland=True,
        landcolor="rgb(243, 243, 243)",
        showcoastlines=True, coastlinecolor="Black",
        showlakes=True, lakecolor="rgba(173, 216, 230, 0.7)",  # Kolor jezior z przezroczystością
        coastlinewidth=2,  # Grubość linii brzegowej
        projection_scale=6,  # Zmiana skali projekcji, jeśli to konieczne
    ),
    font=dict(family="Arial", size=14),  # Ustawienie czcionki
    margin={"r":0,"t":40,"l":0,"b":0},  # Mniejsze marginesy
)

# Wyświetlamy mapę
fig.show()
