import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import astropy.time as mytm
import astropy.io.fits as fitsio
from matplotlib.dates import DateFormatter
from datetime import datetime
from sqlalchemy import create_engine
from TSI_PLOT_LIB_JTSIM_pandas import create_HKfig, create_Irradfig, plot_HK_1, plot_HK_2, plot_SCI_1 

# https://stackoverflow.com/questions/5734438/how-to-create-a-month-iterator
def month_year_iter( start_month, start_year, end_month, end_year ):
    ym_start= 12*start_year + start_month - 1
    ym_end= 12*end_year + end_month - 1
    for ym in range( ym_start, ym_end ):
        year, month = divmod( ym, 12 )
        yield year, month+1

hk_plotPostFix = "HK_Plot_custom.png"
rad_plotPostFix = "RAD_Plot_custom.png"
save_folder = './plots/custom/'

# hk_plotPostFix = "_HK_Plot.pdf"
# rad_plotPostFix = "_RAD_Plot.pdf"

version = " / 0.1"

conn_string = "mysql+mysqlconnector://dev:password@localhost:3306/test_db"
conn_string = "mysql+mysqlconnector://dara_dev:password@localhost:3306/dara"
# conn_string = "mysql+mysqlconnector://dara_dev:password@localhost:3306/data_test"

engine = create_engine(
    conn_string
)

start_year = 2022
start_month = 6
end_year = 2022
end_month = 12

start_date = '2022-06-02'
end_date = '2022-07-17'

start_date = '2022-06-02'
end_date = '2022-06-10'

# start_date = '2022-06-02 00:00:00'
# end_date = '2022-06-02 11:11:11'

print(f'----- {start_date} to {end_date} -----')
housekeeping_query = f"SELECT * FROM housekeeping WHERE timestamp BETWEEN '{start_date}' and '{end_date}' order by timestamp;"
df_housekeeping = pd.read_sql(housekeeping_query, con=engine)
df_housekeeping.columns = map(str.lower, df_housekeeping.columns)
print("Finish loading data from DB")
print(f"Rows loaded {len(df_housekeeping)}")

calibration_query = f"SELECT * FROM calibration WHERE timestamp BETWEEN '{start_date}' and '{end_date}' order by timestamp;"
df_calibration = pd.read_sql(calibration_query, con=engine)
df_calibration.columns = map(str.lower, df_calibration.columns)
print("Finish loading data from DB")
print(f"Rows loaded {len(df_calibration)}")

cavity_map = {"a": 1, "A": 1, "b": 2, "B": 2, "c": 3, "C":3, "none": 0, None: 0}
df_calibration["nominal_cavity"] = df_calibration["nominal_cavity"].map(
    lambda x: cavity_map.get(x, 0)
).astype(np.uint8)
df_calibration["reference_cavity"] = df_calibration["reference_cavity"].map(
    lambda x: cavity_map.get(x, 0)
).astype(np.uint8)
df_calibration["backup_cavity_1"] = df_calibration["backup_cavity_1"].map(
    lambda x: cavity_map.get(x, 0)
).astype(np.uint8)


plotname = '_'.join([start_date, 'to', end_date, "01", hk_plotPostFix])
print(f"plotname: {plotname}")
# day_data = df_resampled[df_resampled["timestamp"].dt.date == day]
fig, ax = create_HKfig("FY-3 JTSIM DARA HK " + plotname + version)
plot_HK_1(df_housekeeping, ax, "custom")
plotname = plotname.replace(':','_')
fig.savefig(save_folder + plotname)
plt.close(fig)
    
plotname = '_'.join([start_date, 'to', end_date, "02", hk_plotPostFix])
print(f"plotname: {plotname}")
fig, ax = create_HKfig("FY-3 JTSIM DARA HK " + plotname + version)
plot_HK_2(df_housekeeping, ax, "custom")
plotname = plotname.replace(':','_')
fig.savefig(save_folder + plotname)
plt.close(fig)

plotname = '_'.join([start_date, 'to', end_date, "03", rad_plotPostFix])
print(f"plotname: {plotname}")
# fig, ax = create_HKfig("FY-3 JTSIM DARA RAD " + plotname + version)
fig, ax = create_Irradfig("FY-3 JTSIM DARA RAD " + plotname + version)
plot_SCI_1(df_calibration, ax, "custom")
plotname = plotname.replace(':','_')
fig.savefig(save_folder + plotname)
plt.close(fig)
