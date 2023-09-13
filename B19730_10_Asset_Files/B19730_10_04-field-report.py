import folium
import requests
import json

def read_bin(api_key, bin_id):
    url = f"https://api.jsonbin.io/v3/b/{bin_id}/latest"
    headers = {
        "X-Master-Key": api_key
    }   
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()["record"]
    else:
        print(f"Failed to read bin: {response.status_code}")
        print(response.json())
        return None

def add_geojson_to_map(geojson, map_obj):
    def style_function(feature):
        return {'fillColor': '#ffaf00', 'color': 'blue', 'weight': 1.5}
    
    folium.GeoJson(
        geojson,
        style_function=style_function,
        popup=folium.GeoJsonPopup(fields=list(geojson['features'][0]['properties'].keys()))
    ).add_to(map_obj)

def get_bounds(geojson):
    coordinates = []
    for feature in geojson['features']:
        coords = feature['geometry']['coordinates']
        coordinates.append([coords[1], coords[0]])  # Flip to [lat, lon]
    return coordinates

api_key = "$2b$10$lypZoIQPtYtz1PTSk75KjuzUGMnupW1pSJdqtU.wSnmXuGZTDjIpy"  # Replace with your actual JSONBin.io API key
bin_id = "64fe6ae18d92e126ae6a1a23" 

m = folium.Map()

geojson = read_bin(api_key, bin_id)

add_geojson_to_map(geojson, m)

# Get bounds of all points and fit the map to show all
bounds = get_bounds(geojson)
m.fit_bounds(bounds)

m.save("map.html")
