import pandas as pd

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

df_tascas = pd.read_csv("data/raw/tascas_lisbon_initial.csv") 
df_tascas['neighbourhood'] = df_tascas['neighbourhood'].apply(clean_neighborhood_name)

# Drop rows missing coordinates
df_tascas = df_tascas.dropna(subset=['lat', 'lng'])

# Remove exact duplicates based on name + address
df_tascas = df_tascas.drop_duplicates(subset=['name', 'address'])

print(f"Total rows: {len(df_tascas)}")
print(f"Missing (NaN) count: {df_tascas['price_level'].isna().sum()}")
print(f"Percentage missing: {(df_tascas['price_level'].isna().sum() / len(df_tascas)) * 100:.2f}%")

#Compute median price
median_price = df_tascas['price_level'].median()
if pd.isna(median_price): median_price = 2.0
df_tascas['price_level'] =df_tascas['price_level'].fillna(median_price)



# Verify no NaNs remain
print(f"Remaining NaNs after fill: {df_tascas['price_level'].isna().sum()}")

print(f"Clean dataset: {len(df_tascas)} unique restaurants")
df_filled.to_csv("data/cleaned/cleaned_tascas.csv", index=False)