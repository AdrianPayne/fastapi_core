import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the dataset
dataset_path = 'services/mobile_signal/data/mobile_signal_dataset.csv'
data = pd.read_csv(dataset_path)

# Get the latitude, longitude, and RSSI values
latitude = data['Latitude']
longitude = data['Longitude']
rssi = data['RSSI']

# Print the minimum and maximum values
print('Minimum latitude:', np.min(latitude))
print('Maximum latitude:', np.max(latitude))
print('Minimum longitude:', np.min(longitude))
print('Maximum longitude:', np.max(longitude))

# Create a 2D heatmap of the RSSI values
plt.hexbin(longitude, latitude, C=rssi, gridsize=50, cmap='viridis', bins=None)
plt.colorbar()
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('2D Heatmap of Latitude, Longitude, and RSSI')
plt.show()
