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
)


hk_plotPostFix = "_HK_Plot_lifetime.png"
rad_plotPostFix = "_RAD_Plot_lifetime.png"
save_folder = "./plots/lifetime/"

# hk_plotPostFix = "_HK_Plot.pdf"
# rad_plotPostFix = "_RAD_Plot.pdf"

version = " / 0.1"

conn_string = "mysql+mysqlconnector://dev:password@localhost:3306/test_db"
conn_string = "mysql+mysqlconnector://dara_dev:password@localhost:3306/dara"

engine = create_engine(conn_string)

housekeeping_query = "SELECT * FROM housekeeping WHERE timestamp is not NULL order by timestamp;"
df_housekeeping = pd.read_sql(housekeeping_query, con=engine)
df_housekeeping.columns = map(str.lower, df_housekeeping.columns)
print("Finish loading data from DB")
print(f"Rows loaded {len(df_housekeeping)}")

calibration_query = "SELECT * FROM calibration WHERE timestamp is not null order by timestamp;"
df_calibration = pd.read_sql(calibration_query, con=engine)
df_calibration.columns = map(str.lower, df_calibration.columns)
print("Finish loading data from DB")
print(f"Rows loaded {len(df_calibration)}")

cavity_map = {"a": 1, "A": 1, "b": 2, "B": 2, "c": 3, "C":3, "none": 0, None: 0}
df_calibration["nominal_cavity"] = (
    df_calibration["nominal_cavity"]
    .map(lambda x: cavity_map.get(x, 0))
    .astype(np.uint8)
)
df_calibration["reference_cavity"] = (
    df_calibration["reference_cavity"]
    .map(lambda x: cavity_map.get(x, 0))
    .astype(np.uint8)
)
df_calibration["backup_cavity_1"] = (
    df_calibration["backup_cavity_1"]
    .map(lambda x: cavity_map.get(x, 0))
    .astype(np.uint8)
)

plotname = "01" + hk_plotPostFix
print(f"plotname: {plotname}")
# day_data = df_resampled[df_resampled["timestamp"].dt.date == day]
fig, ax = create_HKfig("FY-3 JTSIM DARA HK " + plotname + version)
plot_HK_1(df_housekeeping, ax, "lifetime")
fig.savefig(save_folder + plotname)
plt.close(fig)

plotname = "02" + hk_plotPostFix
print(f"plotname: {plotname}")
fig, ax = create_HKfig("FY-3 JTSIM DARA HK " + plotname + version)
plot_HK_2(df_housekeeping, ax, "lifetime")
fig.savefig(save_folder + plotname)
plt.close(fig)
# continue
plotname = "03" + rad_plotPostFix
print(f"plotname: {plotname}")
# fig, ax = create_HKfig("FY-3 JTSIM DARA RAD " + plotname + version)
fig, ax = create_Irradfig("FY-3 JTSIM DARA RAD " + plotname + version)
plot_SCI_1(df_calibration, ax, "lifetime")
fig.savefig(save_folder + plotname)
plt.close(fig)

exit()