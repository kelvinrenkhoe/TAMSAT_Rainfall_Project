# import requests
# import pandas as pd
# import os
# import logging

# # Configure logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# def download_tamsat_data(lat, lon, start_year, end_year, location_name, output_dir="data"):
#     """
#     Downloads TAMSAT rainfall estimates for a given location and time range.
#     """
#     base_url = "https://new-api.tamsat.reading.ac.uk/data/download/"
#     output_file = os.path.join(output_dir, f"{location_name}_rainfall_{start_year}_{end_year}.csv")
#     os.makedirs(output_dir, exist_ok=True)
    
#     data = []
    
#     for year in range(start_year, end_year + 1):
#         url = f"{base_url}?lat={lat}&lon={lon}&year={year}&format=csv"
        
#         response = requests.get(url)
        
#         if response.status_code == 200:
#             yearly_data = response.text.split("\n")
#             for row in yearly_data[1:]:  # Skip header
#                 if row:
#                     date, rainfall = row.split(',')
#                     data.append([date, float(rainfall), location_name, lat, lon])
#         else:
#             logging.error(f"Failed to retrieve data for {location_name} in {year}")
    
#     df = pd.DataFrame(data, columns=["Date", "Rainfall (mm)", "Location", "Latitude", "Longitude"])
#     df.to_csv(output_file, index=False)
#     logging.info(f"Saved data for {location_name} to {output_file}")

# # Define locations and their coordinates
# locations = [
#     ("Abeokuta", 7.1479, 3.3497),
#     ("Epe", 6.5333, 3.5167),
#     ("Fiditi Grammar School", 7.7167, 3.9167),
#     ("Middle Ogun Irrigation Project", 7.8833, 3.75),
#     ("Sepeteri", 8.6281, 3.6448),
#     ("Oyan Dam", 7.25, 3.2667)
# ]

# start_year = 1989
# end_year = 2004
# output_directory = "data"

# # Download data for each location
# for name, lat, lon in locations:
#     download_tamsat_data(lat, lon, start_year, end_year, name, output_directory)

# logging.info("All data downloads completed.")
