import geopandas as gpd
import matplotlib.pyplot as plt
import os
from matplotlib.colors import ListedColormap
import numpy as np

# Define paths
base_path = r"F:\OneDrive\My Projects\Coding\Rent_Project\olx-apartment-scraper\geography"
input_file = os.path.join(base_path, "curitiba_street_polygons.geojson")
output_file = os.path.join(base_path, "curitiba_street_polygons_map.png")

# Load the GeoJSON file
street_polygons = gpd.read_file(input_file)

# Create a color map
unique_classes = street_polygons['fclass'].unique()
n_classes = len(unique_classes)
colors = plt.cm.viridis(np.linspace(0, 1, n_classes))
color_map = ListedColormap(colors)

# Create the plot
fig, ax = plt.subplots(figsize=(20, 20))

# Plot street polygons
street_polygons.plot(ax=ax, column='fclass', cmap=color_map, legend=False, 
                     edgecolor='none', alpha=0.7)

# Remove axis
ax.axis('off')

# Add title
plt.title('Street Polygons of Curitiba', fontsize=20)

# Add scale bar (approximate)
ax.plot([0.05, 0.15], [0.05, 0.05], transform=ax.transAxes, color='black', linewidth=2)
ax.text(0.1, 0.06, '5 km', transform=ax.transAxes, horizontalalignment='center', verticalalignment='bottom')

# Add north arrow
x, y, arrow_length = 0.95, 0.95, 0.05
ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
            arrowprops=dict(facecolor='black', width=5, headwidth=15),
            ha='center', va='center', fontsize=20,
            xycoords=ax.transAxes)

# Create legend
legend_elements = [plt.Rectangle((0, 0), 1, 1, facecolor=color_map(i), edgecolor='none', alpha=0.7) 
                   for i in range(n_classes)]
ax.legend(legend_elements, unique_classes, title='Road Type', 
          loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=3)

# Adjust layout
plt.tight_layout()

# Save the plot
plt.savefig(output_file, dpi=300, bbox_inches='tight')

print(f"Map saved to {output_file}")

# Display some statistics
print(f"Total number of street polygons: {len(street_polygons)}")
print("\nRoad types and their counts:")
print(street_polygons['fclass'].value_counts())

# Calculate total area covered by streets
total_area = street_polygons.to_crs(epsg=31982).area.sum() / 1000000  # Convert to square kilometers
print(f"\nTotal area covered by streets: {total_area:.2f} sq km")

# Show the plot
plt.show()

