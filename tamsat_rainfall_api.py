"""
TAMSAT Download and Extraction API Source Code

Author: TAMSAT (tamsat@reading.ac.uk)
"""

import os
import wget
import numpy as np
import xarray as xr
import itertools
import pandas as pd
import calendar
from datetime import datetime as dt
from datetime import timedelta as td

def date_df(timestep, startdate, enddate, endmonth):
    """
    Create a dataframe of dates and related information for RFE file creation.
    """
    if endmonth:
        enddate_check = pd.to_datetime(enddate, format="%Y-%m-%d")
        if not enddate_check.is_month_end:
            enddate = (pd.to_datetime(enddate, format="%Y-%m-%d") + pd.tseries.offsets.MonthEnd()).strftime("%Y-%m-%d")
    
    start, end = dt.strptime(startdate, "%Y-%m-%d").date(), dt.strptime(enddate, "%Y-%m-%d").date()
    df = pd.date_range(start=start, end=end, name="Date").to_frame(index=False)
    df["Year"], df["Month"], df["Day"], df["DoY"] = df.Date.dt.year, df.Date.dt.month, df.Date.dt.day, df.Date.dt.dayofyear
    
    # Assign Pentads and Dekads
    pentad_bins = [["01", "02", "03", "04", "05"], ["06", "07", "08", "09", "10"],
                   ["11", "12", "13", "14", "15"], ["16", "17", "18", "19", "20"],
                   ["21", "22", "23", "24", "25"], ["26", "27", "28", "29", "30", "31"]]
    dekad_bins = [pentad_bins[:2], pentad_bins[2:4], pentad_bins[4:]]
    df["Pentad"], df["Dekad"] = 0, 0
    for i, days in enumerate(pentad_bins, 1): df.loc[df.Day.astype(str).isin(days), "Pentad"] = i
    for i, group in enumerate(dekad_bins, 1): df.loc[df.Day.astype(str).isin(sum(group, [])), "Dekad"] = i
    
    # Assign Seasons
    seasons = {"DJF": [12, 1, 2], "MAM": [3, 4, 5], "JJA": [6, 7, 8], "SON": [9, 10, 11]}
    df["Season"] = df.Month.map(lambda m: next((s for s, months in seasons.items() if m in months), None))
    return df

def check_dates(startdate, enddate):
    """Validate the date format."""
    try:
        dt.strptime(startdate, "%Y-%m-%d")
        dt.strptime(enddate, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def check_lonlat(lon, lat):
    """Check if the longitude and latitude values are within the TAMSAT domain."""
    return -19.0125 <= lon <= 51.975 and -35.9625 <= lat <= 38.025

def download_files(file_urls, local_dir):
    """Download TAMSAT files to a specified directory."""
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
    for url in file_urls:
        file_path = os.path.join(local_dir, os.path.basename(url))
        if not os.path.exists(file_path):
            wget.download(url, file_path)

def get_filenames(remoteurl, dates, timestep, version):
    """Generate file URLs based on date range and timestep."""
    return [f"{remoteurl}/v{version}/{timestep}/{d.strftime('%Y/%m')}/rfe{d.strftime('%Y_%m_%d')}.v{version}.nc" for d in dates]

# TAMSAT data URL
remoteurl = 'http://gws-access.jasmin.ac.uk/public/tamsat/rfe'