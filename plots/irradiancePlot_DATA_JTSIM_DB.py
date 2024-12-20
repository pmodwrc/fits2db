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
    create_irradiance_fig,
    plot_HK_1,
    plot_HK_2,
    plot_SCI_1,
    plot_irr,
    plot_parameter,
)


hk_plotPostFix = "_HK_Plot.png"
rad_plotPostFix = "_RAD_Plot.png"
save_folder = "./plots/lifetime/"

# hk_plotPostFix = "_HK_Plot.pdf"
# rad_plotPostFix = "_RAD_Plot.pdf"

version = " / 0.1"

conn_string = "mysql+mysqlconnector://dev:password@localhost:3306/test_db"
conn_string = "mysql+mysqlconnector://dara_dev:password@localhost:3306/dara"

engine = create_engine(conn_string)

irradiance_query = """SELECT 
    `timestamp`, `irradiance_a_wm2_`, `irradiance_b_wm2_`, `irradiance_c_wm2_`
    FROM irradiance
    WHERE timestamp is not null order by timestamp;"""
df_irradiance = pd.read_sql(irradiance_query, con=engine)
df_irradiance.columns = map(str.lower, df_irradiance.columns)
print("Finish loading data from DB")
print(f"Rows loaded {len(df_irradiance)}")

plotname = "total_irradiance.png"
print(f"plotname: {plotname}")
    # day_data = df_resampled[df_resampled["timestamp"].dt.date == day]
fig, ax = create_irradiance_fig("FY-3 JTSIM DARA Irradiance " + plotname + version)
plot_irr(df_irradiance, ax, "year")
fig.savefig(save_folder + plotname)
plt.close(fig)

parameter_query = """SELECT
    * FROM `parameterset` WHERE timestamp is not null"""
df_parameter = pd.read_sql(parameter_query, con=engine)
df_parameter.columns = map(str.lower, df_parameter.columns)
print("Finish loading data from DB")
print(f"Rows loaded {len(df_parameter)}")

plotname = "total_parameterset.png"
print(f"plotname: {plotname}")
fig, ax = create_HKfig("FY-3 " + plotname + version)
plot_parameter(df_parameter, ax)
fig.savefig(save_folder + plotname)
plt.close(fig)
