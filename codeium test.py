import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV
data = pd.read_csv('data.csv', skiprows=4)

# Extract the latitude and longitude columns
lat = data['lat']
lon = data['lon']

# Create a scatter plot of the data
plt.scatter(lon, lat)

# Add a sprite of a boat
boat_image = plt.imread('boat.png')
plt.imshow(boat_image, extent=[min(lon), max(lon), min(lat), max(lat)], interpolation='bilinear')

# Add a sprite of a sail
sail_image = plt.imread('sail.png')
plt.imshow(sail_image, extent=[min(lon), max(lon), min(lat), max(lat)], interpolation='bilinear')

# Show the plot
plt.show()
