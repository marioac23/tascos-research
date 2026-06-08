import googlemaps
API_KEY = "AIzaSyCmq6mCAce_Blt02BsCL_NQwZlGKgqKuh0"
gmaps = googlemaps.Client(key=API_KEY)

# Test ONE coordinate
lat, lng = 38.7127703,-9.126521900000002 # Replace with one from your CSV
result = gmaps.reverse_geocode((lat, lng))

# Print ALL address components to see what's available
print(result['administrative_area_level_3'])