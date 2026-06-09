import googlemaps
import pandas as pd
import time
import argparse

# PUT YOUR KEY HERE - KEEP THIS FILE PRIVATE!
API_KEY = "AIzaSyCmq6mCAce_Blt02BsCL_NQwZlGKgqKuh0"

gmaps = googlemaps.Client(key=API_KEY)
def get_neighbourhood(lat, lng):
    """Helper to find 'administrative_area_level_3' (Freguesia) using Reverse Geocoding"""
    try:
        result = gmaps.reverse_geocode((lat, lng))
        if not result:
            return "Unknown"
        
        for component in result[0]['address_components']:
            # Look specifically for the type you found earlier
            if 'administrative_area_level_3' in component['types']:
                return component['long_name']
            
            # Fallback to sublocality if level 3 is missing
            if 'sublocality' in component['types']:
                return component['long_name']
                
        return "Unknown"
    except Exception as e:
        print(f"Error getting freguesia for {lat}, {lng}: {e}")
        return "Unknown"
    
def search_tascas(latitude, longitude, keyword, radius=50000):
    """Search for traditional Portuguese eateries"""
    all_results = []

    response = gmaps.places_nearby(
                location=(latitude, longitude),
                radius=radius,
                keyword=keyword,
                language='pt'
            )
            
    all_results.extend(response.get('results', []))
    next_page_token = response.get('next_page_token')

    #Paginate through results
    max_pages = 5  # Safety limit to avoid quota exhaustion
    page_count = 0
    while page_count < max_pages:
        print(f'Fetching next page... ({len(all_results)} results)')
        time.sleep(2)
        
        response = gmaps.places_nearby(
            location=(latitude, longitude),
            radius=radius,
            keyword=keyword,
            page_token=next_page_token  # Fallback
        )
        
        page_count+=1
        time.sleep(2.5)  # Be polite: respect rate limits
        new_results = response.get('results', [])
        if not new_results:
            break

        all_results.extend(new_results)
        next_page_token = response.get('next_page_token')
        if not next_page_token:
            break

    return all_results


parser = argparse.ArgumentParser(description="Arguments for running code",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-loc", "--location", default=None, type = str, help="where to look")
parser.add_argument("-o", "--output", default=None, type = str, help="output file")


args = vars(parser.parse_args())


location    = args["location"]
output      = args["output"]


lat = 0 
lon = 0
if location=="lisbon":
    lat = 38.722252
    lon = -9.139337
elif location=="porto":
    lat = 41.158461
    long = -8.632595
# Run the search
KEYWORDS_HIGH_DATA = [
    "fine dining", 
    "gourmet restaurant", 
    "buffet restaurant", 
    "churrascaria", # Steakhouses usually have prices
    "seafood restaurant",
    "restaurant",   # Broad catch-all
]
keywords = ["fine dining", 
    "gourmet restaurant", 
    "buffet restaurant", 
    "churrascaria", # Steakhouses usually have prices
    "seafood restaurant",
    "restaurant"]#"tasco", "tasca", "taberna", "petiscos", "restaurante"]
all_raw_data = []

for kw in keywords:
    print(f"\n=== Searching: {kw} ===")
    raw_results = search_tascas(lat, lon, kw, 50000)
    for place in raw_results:
        # Get Details (Name, Address, Rating, Price, Status)
        try:
            details = gmaps.place(place_id=place['place_id'], fields=[
                'name', 'formatted_address', 'rating', 'price_level', 
                'business_status', 'reviews'
            ])
            res = details.get('result', {})
            
            # Get Neighborhood
            neighbourhood = get_neighbourhood(
                place['geometry']['location']['lat'], 
                place['geometry']['location']['lng']
            )
            
            # --- SAVE ONLY YOUR REQUESTED FIELDS ---
            result_data = {
                'name': res.get('name'),
                'address': res.get('formatted_address'),
                'neighbourhood': neighbourhood,
                'latitude': place['geometry']['location']['lat'],
                'longitude': place['geometry']['location']['lng'],
                'rating': res.get('rating', 'N/A'),
                'price_level': res.get('price_level', 'N/A'),
                'reviews_count': len(res.get('reviews', [])),
                'status': res.get('business_status'),
                'search_keyword': kw
            }
            
            all_raw_data.append(result_data)
            
        except Exception as e:
            print(f"Skipping place {place.get('name')}: {e}")
        
        time.sleep(0.2) # Rate limit safety

# --- CLEANUP & SAVE ---
print("\n--- Processing Data ---")
df = pd.DataFrame(all_raw_data)

# Remove duplicates based on Place ID logic (Name + Address)
df_unique = df.drop_duplicates(subset=['name', 'address'])

# Save to CSV immediately
df_unique.to_csv("data/raw/"+output, index=False)

print(f"\n✅ DONE!")
print(f"Total unique restaurants saved: {len(df_unique)}")
print(f"File saved to: {output}")
print("\nColumns saved:", list(df_unique.columns))
