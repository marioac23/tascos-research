import googlemaps
import pandas as pd
import time

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
    
def search_tascas(latitude, longitude, keywords=["tasco", "tasca", "taberna", "petiscos", "restaurante"], radius=50000):
    """Search for traditional Portuguese eateries"""
    results = []
    for keyword in keywords:
        try:
            response = gmaps.places_nearby(
                location=(latitude, longitude),
                radius=radius,
                keyword=keyword,
                language='pt'
            )
            
            for place in response.get('results', []):
                # Get extended details for each place
                place_details = gmaps.place(
                    place_id=place['place_id'],
                    fields=['name', 'rating', 'price_level', 'formatted_address', 'reviews', 'business_status']
                )

                neighborhood = get_neighbourhood(
                    place['geometry']['location']['lat'], 
                    place['geometry']['location']['lng']
                )
                
                result_data = {
                    'name': place_details['result'].get('name'),
                    'address': place_details['result'].get('formatted_address'),
                    'neighbourhood': neighborhood,
                    'lat': place['geometry']['location']['lat'],
                    'lng': place['geometry']['location']['lng'],
                    'rating': place_details['result'].get('rating', 'N/A'),
                    'price_level': place_details['result'].get('price_level', 'N/A'),
                    'reviews_count': len(place_details['result'].get('reviews', [])),
                    'status': place_details['result'].get('business_status'),
                    'search_keyword': keyword
                }
                
                results.append(result_data)
                
            time.sleep(0.1)  # Be polite: respect rate limits
            
        except Exception as e:
            print(f"Error searching {keyword}: {e}")
    
    return pd.DataFrame(results)
lisbon_lat = 38.722252
lisbon_lon = -9.139337
# Run the search
df = search_tascas(latitude=lisbon_lat, longitude=lisbon_lon)

# Save to CSV immediately
df.to_csv("data/raw/tascas_lisbon_initial.csv", index=False)
print(f"Saved {len(df)} restaurants")