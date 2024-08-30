import geopandas as gpd
import os
from shapely.geometry import box

# Define paths
base_path = r"F:\OneDrive\My Projects\Coding\Rent_Project\olx-apartment-scraper\geography"
neighborhoods_file = os.path.join(base_path, "neighborhoods", "DIVISA_DE_BAIRROS.shp")
roads_file = os.path.join(base_path, "OSM", "sul-latest-free.shp", "gis_osm_roads_free_1.shp")

def preview_shapefile(file_path, name):
    print(f"\n--- Preview of {name} data ---")
    gdf = gpd.read_file(file_path)
    
    print(f"Number of records: {len(gdf)}")
    print("\nColumns and their data types:")
    print(gdf.dtypes)
    
    print("\nFirst few rows (excluding geometry):")
    print(gdf.drop(columns='geometry').head())
    
    print("\nUnique values in each column:")
    for column in gdf.columns:
        if column != 'geometry':
            unique_values = gdf[column].nunique()
            print(f"{column}: {unique_values} unique values")
    
    return gdf

# Preview neighborhoods data
neighborhoods = preview_shapefile(neighborhoods_file, "Neighborhoods")

# Preview roads data
# We'll use the same bounding box as before to filter for Curitiba
curitiba_bbox = box(-49.3900, -25.5800, -49.1900, -25.3800)
roads = gpd.read_file(roads_file, bbox=curitiba_bbox)
preview_shapefile(roads_file, "Roads (filtered for Curitiba)")

# Additional analysis for roads
print("\n--- Additional Roads Data Analysis ---")
print("\nRoad types and their counts:")
print(roads['fclass'].value_counts())

print("\nSample of road names:")
print(roads['name'].sample(10))

print("\nTotal length of roads:")
roads['length_km'] = roads.geometry.length / 1000  # Convert to kilometers
print(f"{roads['length_km'].sum():.2f} km")

print("\nLongest roads:")
print(roads.sort_values('length_km', ascending=False)[['name', 'fclass', 'length_km']].head())