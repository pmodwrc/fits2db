import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import astropy.time as mytm
import astropy.io.fits as fitsio
from matplotlib.dates import DateFormatter
from datetime import datetime
from sqlalchemy import create_engine
from TSI_PLOT_LIB_JTSIM_pandas import (
    create_HKfig,
    create_Irradfig,
    plot_HK_1,
    plot_HK_2,
    plot_SCI_1,
    convert_cavity_to_numeric,
    plot_HK_1_from_cfg
)


import yaml

with open('hk1.yml', 'r') as f:
    cfg = yaml.safe_load(f)

hk_plotPostFix = "_HK_Plot.png"
rad_plotPostFix = "_RAD_Plot.png"
save_folder = "./plots/daily/"

# hk_plotPostFix = "_HK_Plot.pdf"
# rad_plotPostFix = "_RAD_Plot.pdf"

version = " / 0.1"

conn_string = "mysql+mysqlconnector://dev:password@localhost:3306/test_db"
conn_string = "mysql+mysqlconnector://dara_dev:password@localhost:3306/dara"

engine = create_engine(conn_string)

start_year = 2023
start_month = 4
start_day = 1
end_year = 2023
end_month = 4
end_day = 30

# query = f"""
# SELECT * FROM `HOUSEKEEPING`
# WHERE `YEAR` = {start_year}
# AND `MONTH` = {start_month}
# AND `DAY` BETWEEN {start_day} AND {end_day};
# """
query = f"""
SELECT * FROM housekeeping WHERE timestamp 
between '{start_year}-{start_month:02d}-{start_day:02d}' 
and '{end_year}-{end_month:02d}-{end_day:02d}';"""

calibration_query = f"""
SELECT * FROM calibration WHERE timestamp 
between '{start_year}-{start_month:02d}-{start_day:02d}' 
and '{end_year}-{end_month:02d}-{end_day:02d}';"""

# print("Start loading data from DB")
df_sql = pd.read_sql(query, con=engine)
df_calibration = pd.read_sql(calibration_query, con=engine)
print("Finish loading data from DB")
print(f"Rows loaded {len(df_sql)}")
df_sql["timestamp"] = pd.to_datetime(df_sql["timestamp"])
# df_resampled = df_sql.resample("min", on="timestamp").mean().reset_index()
df_resampled = df_sql
df_calibration.columns = map(str.lower, df_calibration.columns)
df_resampled.columns = map(str.lower, df_resampled.columns)

# import ipdb; ipdb.set_trace()
# cavity_map = {"a": 1, "A": 1, "b": 2, "B": 2, "c": 3, "C":3, "none": 0, None: 0}
# df_calibration["nominal_cavity"] = df_calibration["nominal_cavity"].map(
# lambda x: cavity_map.get(x, 0)
# ).astype(np.uint8)
# df_calibration["reference_cavity"] = df_calibration["reference_cavity"].map(
# lambda x: cavity_map.get(x, 0)
# ).astype(np.uint8)
# df_calibration["backup_cavity_1"] = df_calibration["backup_cavity_1"].map(
# lambda x: cavity_map.get(x, 0)
# ).astype(np.uint8)
df_calibration = convert_cavity_to_numeric(df_calibration)
# df_calibration_resampled = df_calibration.resample("min", on="timestamp").mean().reset_index()
df_calibration_resampled = df_calibration

for day in df_resampled["timestamp"].dt.date.unique():
    plotname = str(day).replace("-", "_") + "_1_gen_" + hk_plotPostFix
    print(f"plotname: {plotname}")
    day_data = df_resampled[df_resampled["timestamp"].dt.date == day]
    fig, ax = create_HKfig("FY-3 JTSIM DARA HK " + plotname + version)
    # plot_HK_1(day_data, ax, "day")
    plot_HK_1_from_cfg(day_data, ax, "day", cfg)
    fig.savefig(save_folder + plotname)
    plt.close(fig)

    plotname = str(day).replace("-", "_") + "_1" + hk_plotPostFix
    print(f"plotname: {plotname}")
    day_data = df_resampled[df_resampled["timestamp"].dt.date == day]
    fig, ax = create_HKfig("FY-3 JTSIM DARA HK " + plotname + version)
    plot_HK_1(day_data, ax, "day")
    fig.savefig(save_folder + plotname)
    plt.close(fig)

    plotname = str(day).replace("-", "_") + "_2" + hk_plotPostFix
    print(f"plotname: {plotname}")
    day_data = df_resampled[df_resampled["timestamp"].dt.date == day]
    fig, ax = create_HKfig("FY-3 JTSIM DARA HK " + plotname + version)
    plot_HK_2(day_data, ax, "day")
    fig.savefig(save_folder + plotname)
    plt.close(fig)
    # continue
    plotname = str(day).replace("-", "_") + "_3" + rad_plotPostFix
    print(f"plotname: {plotname}")
    day_data = df_calibration_resampled[
        df_calibration_resampled["timestamp"].dt.date == day
    ]
    # fig, ax = create_HKfig("FY-3 JTSIM DARA RAD " + plotname + version)
    fig, ax = create_Irradfig("FY-3 JTSIM DARA RAD " + plotname + version)
    plot_SCI_1(day_data, ax, "day")
    fig.savefig(save_folder + plotname)
    plt.close(fig)
