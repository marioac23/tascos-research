import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import numpy as np
import folium

df_tascas = pd.read_csv('data/raw/rest_lisbon_initial.csv')
df_airbnb = pd.read_csv("data/raw/listings_lisbon.csv")

plt.figure()
plt.scatter(df_tascas['longitude'], df_tascas['latitude'], label='tascas')
plt.scatter(df_airbnb['longitude'], df_airbnb['latitude'], label='airbnb', alpha=0.5)
plt.legend()
plt.savefig('results/map.png')

# Create a map centered on Lisbon
m = folium.Map(location=[38.7223, -9.1393], zoom_start=12)

# Add markers
for _, row in df_tascas.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=row['name'],
        icon=folium.Icon(color='red', icon='cutlery', prefix='fa')
    ).add_to(m)



# Save as HTML
m.save("results/lisbon_tascas_interactive.html")

print("✅ Interactive map saved! Open 'lisbon_tascas_interactive.")