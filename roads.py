import geopandas as gpd
import matplotlib.pyplot as plt
import os
from shapely.geometry import box

# Define the base path
base_path = r"F:\OneDrive\My Projects\Coding\Rent_Project"

# Function to get city bounds (replace with actual coordinates for your city)
def get_city_bounds(city_name):
    # These are example coordinates for Curitiba
    # Replace these with the actual coordinates of the city you're interested in
    if city_name.lower() == "curitiba":
        return (-49.3900, -25.5800, -49.1900, -25.3800)
    else:
        raise ValueError(f"Bounds for {city_name} not defined. Please add them to the function.")

# Set the city you want to visualize
city_name = "Curitiba"  # Change this to your city of interest

# Get city bounds
minx, miny, maxx, maxy = get_city_bounds(city_name)

# Create a bounding box
bbox = box(minx, miny, maxx, maxy)

# Read the roads shapefile
roads_file = os.path.join(base_path, "sul-latest-free.shp", "gis_osm_roads_free_1.shp")
roads = gpd.read_file(roads_file, bbox=bbox)

# Width multiplier
width_multiplier = 2  # Increase this value to make streets wider

# Create a color and width mapping for different road types
road_styles = {
    'motorway': ('red', 2.5 * width_multiplier),
    'trunk': ('orange', 2 * width_multiplier),
    'primary': ('yellow', 1.5 * width_multiplier),
    'secondary': ('green', 1 * width_multiplier),
    'tertiary': ('blue', 0.75 * width_multiplier),
    'residential': ('purple', 0.5 * width_multiplier),
    'other': ('gray', 0.25 * width_multiplier)
}

# Create the plot
fig, ax = plt.subplots(figsize=(15, 15))

# Plot each road type
for road_type, (color, width) in road_styles.items():
    if road_type != 'other':
        roads[roads['fclass'] == road_type].plot(ax=ax, color=color, linewidth=width, label=road_type)
    else:
        # Plot all other road types
        mask = ~roads['fclass'].isin([k for k in road_styles.keys() if k != 'other'])
        roads[mask].plot(ax=ax, color=color, linewidth=width, label=road_type)

# Customize the plot
ax.set_title(f'Street Network in {city_name}', fontsize=20)
ax.axis('off')
plt.legend(title='Road Types', title_fontsize='13', fontsize='10')

# Show the plot
plt.tight_layout()
plt.show()

# Print some statistics
print(f"Road network statistics for {city_name}:")
print(roads['fclass'].value_counts())
print(f"\nTotal number of road segments: {len(roads)}")
print(f"Total length of roads: {roads.length.sum() / 1000:.2f} km")