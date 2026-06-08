import pandas as pd

df = pd.read_csv("data/raw/tascas_lisbon_initial.csv") 

# Drop rows missing coordinates
df = df.dropna(subset=['lat', 'lng'])

# Remove exact duplicates based on name + address
df = df.drop_duplicates(subset=['name', 'address'])

print(f"Total rows: {len(df)}")
print(f"Missing (NaN) count: {df['price_level'].isna().sum()}")
print(f"Percentage missing: {(df['price_level'].isna().sum() / len(df)) * 100:.2f}%")

# 3. Calculate the GLOBAL MEDIAN of available prices
# This finds the middle value of all non-empty cells
global_median = df['price_level'].median()
print(f"Global Median Price Level (used for filling): {global_median}")

# 4. FILL the missing values (NaN) with the global median
df_filled = df.copy()
df_filled['price_level'] = df_filled['price_level'].fillna(global_median)

# Verify no NaNs remain
print(f"Remaining NaNs after fill: {df_filled['price_level'].isna().sum()}")

print(f"Clean dataset: {len(df_filled)} unique restaurants")
df_filled.to_csv("data/cleaned/cleaned_tascas.csv", index=False)