import os
import csv

# Folder that contains the CSV files
csv_folder = 'services/mobile_signal/data/mobile_dataset'

# Columns to extract from each CSV file
columns = ['Longitude', 'Latitude', 'RSSI']

# List to store extracted data
data = []

# Get the names of the CSV files in the folder
csv_files = [file for file in os.listdir(csv_folder) if file.endswith('.csv')]

# Open each CSV file and extract the specified columns
for file in csv_files:
    with open(os.path.join(csv_folder, file), 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Replace "-" values with None
            cleaned_row = {col: row[col] if row[col] != "-" else None for col in row.keys()}
            data.append([cleaned_row[col] for col in columns])

# Create a new CSV file with the extracted columns
with open('mobile_signal_dataset.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(columns)
    for row in data:
        writer.writerow(row)
