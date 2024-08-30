import geopandas as gpd
import folium
from shapely.geometry import box
import os

# Define paths
base_path = r"F:\OneDrive\My Projects\Coding\Rent_Project\olx-apartment-scraper\geography"
neighborhoods_file = os.path.join(base_path, "neighborhoods", "DIVISA_DE_BAIRROS.shp")
roads_file = os.path.join(base_path, "OSM", "sul-latest-free.shp", "gis_osm_roads_free_1.shp")

# Load neighborhoods data
neighborhoods = gpd.read_file(neighborhoods_file)

# Define Curitiba's bounding box (you may need to adjust these coordinates)
curitiba_bbox = box(-49.3900, -25.5800, -49.1900, -25.3800)

# Load and filter roads data for Curitiba
roads = gpd.read_file(roads_file, bbox=curitiba_bbox)

# Ensure both datasets are in the same CRS (WGS84)
neighborhoods = neighborhoods.to_crs(epsg=4326)
roads = roads.to_crs(epsg=4326)

# Calculate the center of Curitiba
center_lat = neighborhoods.geometry.centroid.y.mean()
center_lon = neighborhoods.geometry.centroid.x.mean()

# Create a map
m = folium.Map(location=[center_lat, center_lon], zoom_start=11)

# Add neighborhoods to the map
folium.GeoJson(
    neighborhoods,
    style_function=lambda feature: {
        'fillColor': 'lightblue',
        'color': 'black',
        'weight': 2,
        'fillOpacity': 0.7,
    }
).add_to(m)

# Add roads to the map
folium.GeoJson(
    roads,
    style_function=lambda feature: {
        'color': 'purple',
        'weight': 1,
        'opacity': 0.7,
    }
).add_to(m)

# Save the map
output_file = os.path.join(base_path, "curitiba_map.html")
m.save(output_file)

print(f"Map saved to {output_file}")