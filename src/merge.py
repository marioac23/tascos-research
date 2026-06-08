import pandas as pd
# Load Airbnb data
airbnb = pd.read_csv("data/raw/listings_lisbon.csv")
tasca = pd.read_csv("data/cleaned/cleaned_tascas.csv")
# Extract neighborhood from Tasa addresses (or use reverse geocoding later)
# For now, let's assume you can map lat/lng to neighborhood manually or via a simple lookup

# Example: Count Airbnbs per neighborhood
airbnb_counts = airbnb['neighbourhood'].value_counts().reset_index()
airbnb_counts.columns = ['neighbourhood', 'airbnb_count']


tasca['price_level'] = pd.to_numeric(tasca['price_level'], errors='coerce')
# Group by neighborhood and calculate statistics
tasca_price_stats = tasca.groupby('neighbourhood').agg({
    'name': 'count',            # Count of Tascas
    'price_level': 'mean',      # Average price level
    'rating': 'mean',           # Bonus: average rating too
    'reviews_count': 'mean'     # Bonus: average reviews
}).reset_index()

# Rename columns for clarity
tasca_price_stats.rename(columns={
    'name': 'tascas_count',
    'price_level': 'avg_price_level',
    'rating': 'avg_rating',
    'reviews_count': 'avg_reviews_count'
}, inplace=True)

merged = airbnb_counts.merge(tasca_price_stats, on='neighbourhood')

print(merged.head())


merged.to_csv("data/cleaned/merged_tasca_airbnb.csv", index=False)
print(f"Saved {len(merged)} restaurants")