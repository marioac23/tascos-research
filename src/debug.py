import googlemaps
import pandas as pd
import time
import numpy as np

API_KEY = "AIzaSyCmq6mCAce_Blt02BsCL_NQwZlGKgqKuh0"
gmaps = googlemaps.Client(key=API_KEY)

LAT, LON = 38.7223, -9.1393  # Lisbon Center

df=pd.read_csv('data/raw/rest_50_lisbon_initial.csv')


def drop_accented_vowels(text):
    if pd.isna(text):
        return text
    
    # List of all Portuguese accented vowels to remove completely
    chars_to_remove = set(['á', 'à', 'â', 'ã', 'ä', 
                           'é', 'è', 'ê', 'ë', 
                           'í', 'ì', 'î', 'ï', 
                           'ó', 'ò', 'ô', 'õ', 'ö', 
                           'ú', 'ù', 'û', 'ü',
                           'Á', 'À', 'Â', 'Ã', 'Ä', 
                           'É', 'È', 'Ê', 'Ë', 
                           'Í', 'Ì', 'Î', 'Ï', 
                           'Ó', 'Ò', 'Ô', 'Õ', 'Ö', 
                           'Ú', 'Ù', 'Û', 'Ü', 'ç', 'Ç'])
    
    result = ""
    for char in str(text).strip():
        if char not in chars_to_remove:
            result += char
    return result.strip()

df['neighbourhood'] = df['neighbourhood'].apply(drop_accented_vowels)

for name in np.unique(df['neighbourhood']):
    print(name)

