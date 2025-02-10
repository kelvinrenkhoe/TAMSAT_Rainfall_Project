import os
import pandas as pd
import xarray as xr

def process_tamsat_data(input_folder, output_file, format='csv'):
    """
    Process manually downloaded TAMSAT rainfall data for Nigeria (1989 - 2004).
    
    Parameters:
    input_folder (str): Path to the folder containing downloaded TAMSAT files.
    output_file (str): Path to save the processed CSV file.
    format (str): File format of the downloaded data ('csv' or 'netcdf').
    """
    all_data = []
    
    for file in os.listdir(input_folder):
        file_path = os.path.join(input_folder, file)
        
        if format == 'csv' and file.endswith('.csv'):
            print(f"Processing {file}...")
            df = pd.read_csv(file_path)
            all_data.append(df)
        
        elif format == 'netcdf' and file.endswith('.nc'):
            print(f"Processing {file}...")
            ds = xr.open_dataset(file_path)
            df = ds.to_dataframe().reset_index()
            all_data.append(df)
    
    # Combine all data into a single dataframe
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        combined_df.to_csv(output_file, index=False)
        print(f"Processed data saved to {output_file}")
    else:
        print("No data files found. Ensure you have downloaded the correct files.")

# Set paths
input_folder = "data/"  # Folder where downloaded files are stored
output_file = "processed_tamsat_nigeria.csv"  # Output file name

# Choose the correct format based on what you downloaded
file_format = "csv"  # Change to 'netcdf' if you downloaded NetCDF files

# Run processing function
process_tamsat_data(input_folder, output_file, format=file_format)
