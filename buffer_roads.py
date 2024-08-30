import geopandas as gpd
from shapely.geometry import box
import os

# Define paths
base_path = r"F:\OneDrive\My Projects\Coding\Rent_Project\olx-apartment-scraper\geography"
roads_file = os.path.join(base_path, "OSM", "sul-latest-free.shp", "gis_osm_roads_free_1.shp")
output_file = os.path.join(base_path, "curitiba_street_polygons.geojson")

# Define Curitiba's bounding box (you may need to adjust these coordinates)
curitiba_bbox = box(-49.3900, -25.5800, -49.1900, -25.3800)

# Load and filter roads data for Curitiba
roads = gpd.read_file(roads_file, bbox=curitiba_bbox)

# Ensure the CRS is in a projected coordinate system for accurate buffering
roads = roads.to_crs(epsg=31982)  # SIRGAS 2000 / UTM zone 22S - suitable for Curitiba

# Create buffer around roads to turn them into polygons
# Adjust the buffer distance as needed (5 meters on each side in this example)
roads['geometry'] = roads.geometry.buffer(5)

# Keep only necessary columns (modify this list as needed)
columns_to_keep = ['name', 'fclass', 'geometry']
roads = roads[columns_to_keep]

# Convert back to WGS84 for standard GeoJSON output
roads = roads.to_crs(epsg=4326)

# Save to GeoJSON
roads.to_file(output_file, driver='GeoJSON')

print(f"Street polygons saved to {output_file}")

# Display some statistics
print(f"Total number of street polygons: {len(roads)}")
print("\nSample of the data:")
print(roads.head())

print("\nColumn names:")
print(roads.columns)

print("\nData types:")
print(roads.dtypes)

print("\nUnique road types:")
print(roads['fclass'].value_counts())