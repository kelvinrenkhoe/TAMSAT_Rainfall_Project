import os
from tamsat_manual_processing import process_tamsat_data

# Define paths
input_folder = "data/"  # Folder where manually downloaded files are stored
output_file = "processed_tamsat_nigeria.csv"  # Output file name

# Choose the format based on what you downloaded (either 'csv' or 'netcdf')
file_format = "csv"  # Change to 'netcdf' if you downloaded NetCDF files

# Ensure the data folder exists
if not os.path.exists(input_folder):
    print(f"Error: Folder '{input_folder}' does not exist. Please ensure you have downloaded the data.")
else:
    # Run the processing function
    process_tamsat_data(input_folder, output_file, format=file_format)
    print("Processing complete. Check the output file.")
