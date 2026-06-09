import pandas as pd
import numpy as np
import argparse

prefix = "União das freguesias de "

def clean_neighborhood_name(name):
    if pd.isna(name):
        return name
    
    name_str = str(name)
    
    # Loop through prefixes and remove if found at the start
    
    if name_str.startswith(prefix):
        name_str = name_str[len(prefix):]
    
    # Optional: Clean up common typos or extra spaces
    name_str = name_str.strip()
    
    return name_str
# the airbnb listing dropped all the accented vowels so this is to do the same for the tascas list
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
parser = argparse.ArgumentParser(description="Arguments for running code",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-i", "--input", default=None, type = str, help="input list of restaurants/tascas")
parser.add_argument("-o", "--output", default=None, type = str, help="output file")


args = vars(parser.parse_args())


input    = args["input"]
output      = args["output"]
# Load data
df_airbnb = pd.read_csv("data/raw/listings_lisbon.csv")
df = pd.read_csv(input)

print(f"=== RAW DATA ===")
print(f"Total rows in CSV: {len(df)}")
print(f"Unique neighborhoods: {df['neighbourhood'].nunique()}")
print(f"NaN neighborhoods: {df['neighbourhood'].isna().sum()}")
print(f"'Unknown' neighborhoods: {(df['neighbourhood'] == 'Unknown').sum()}")
print(f"'N/A' count: {df['price_level'].isna().sum()}")
print(f"Data Type of 'price_level': {df['price_level'].dtype}")
print(f"Unique values in price_level: {df['price_level'].unique()}")
#df['price_level'] = df['price_level'].apply(safe_convert)
df['neighbourhood'] = df['neighbourhood'].apply(clean_neighborhood_name)

# Drop rows missing coordinates
df = df.dropna(subset=['latitude', 'longitude'])

# Remove exact duplicates based on name + address
df = df.drop_duplicates(subset=['name', 'address'])

#Drop nan values
df = df.dropna(subset=['price_level'])
# Make the names the same as the airbnb list
df['neighbourhood'] = df['neighbourhood'].apply(drop_accented_vowels)
print(f'number left {len(df)}')
# Group by neighbourhood
df_stats = df.groupby('neighbourhood').agg({
    'name': 'count',            # Count of dfs
    'price_level': 'mean',      # Average price level
    'rating': 'mean',           # Bonus: average rating too
    'reviews_count': 'mean'     # Bonus: average reviews
}).reset_index()
print(df_stats['neighbourhood'])
# Rename columns for clarity
df_stats.rename(columns={
    'name': 'tascas_count',
    'price_level': 'avg_price_level',
    'rating': 'avg_rating',
    'reviews_count': 'avg_reviews_count'
}, inplace=True)

# Do the same for airbnb
airbnb_stats = df_airbnb.groupby('neighbourhood').agg({
    'name': 'count',            # Count of airbnb
    'number_of_reviews': 'mean'     # Average price level
}).reset_index()

# Rename columns for clarity
airbnb_stats.rename(columns={
    'name': 'airbnb_count',
    'number_of_reviews': 'avg_Nreviews_airbnb'
}, inplace=True)


merged = airbnb_stats.merge(df_stats, on='neighbourhood')

print(merged.head())


merged.to_csv(output, index=False)
print(f"Saved {len(merged)} restaurants")