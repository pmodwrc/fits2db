import argparse
from datetime import datetime

import astropy.io.fits as fitsio
import astropy.time as mytm
import matplotlib.dates as md
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.dates import DateFormatter
from sqlalchemy import create_engine

from TSI_PLOT_LIB_JTSIM_pandas import (
    create_HKfig,
    create_Irradfig,
    plot_HK_1,
    plot_HK_2,
    plot_SCI_1,
    create_irradiance_fig,
    plot_irr,
    plot_parameter,
    convert_cavity_to_numeric,
)


# https://stackoverflow.com/questions/5734438/how-to-create-a-month-iterator
def month_year_iter(start_month, start_year, end_month, end_year):
    ym_start = 12 * start_year + start_month - 1
    ym_end = 12 * end_year + end_month - 1
    for ym in range(ym_start, ym_end):
        year, month = divmod(ym, 12)
        yield year, month + 1


def make_plots(
    dataframes, date_string, plotPostFix, mode, version, save_folder
):
    df_housekeeping = dataframes["housekeeping"]
    plotname = "_".join([date_string, "01_HK_Plot", plotPostFix])
    print(f"plotname: {plotname}")
    # day_data = df_resampled[df_resampled["timestamp"].dt.date == day]
    fig, ax = create_HKfig("FY-3 JTSIM DARA HK 1 " + date_string + version)
    plot_HK_1(df_housekeeping, ax, mode)
    fig.savefig(save_folder + "/" + plotname)
    plt.close(fig)

    plotname = "_".join([date_string, "02_HK_Plot", plotPostFix])
    print(f"plotname: {plotname}")
    fig, ax = create_HKfig("FY-3 JTSIM DARA HK 2 " + date_string + version)
    plot_HK_2(df_housekeeping, ax, mode)
    fig.savefig(save_folder + "/" + plotname)
    plt.close(fig)

    df_calibration = dataframes["calibration"]
    plotname = "_".join([date_string, "RAD_Plot", plotPostFix])
    print(f"plotname: {plotname}")
    # fig, ax = create_HKfig("FY-3 JTSIM DARA RAD " + plotname + version)
    fig, ax = create_Irradfig("FY-3 JTSIM DARA RAD " + date_string + version)
    plot_SCI_1(df_calibration, ax, mode)
    fig.savefig(save_folder + "/" + plotname)
    plt.close(fig)

    df_irradiance = dataframes.get("irradiance", None)
    if df_irradiance is not None:
        plotname = "total_irradiance.png"
        print(f"plotname: {plotname}")
        # day_data = df_resampled[df_resampled["timestamp"].dt.date == day]
        fig, ax = create_irradiance_fig(
            "FY-3 JTSIM DARA Irradiance " + plotname + version
        )
        plot_irr(df_irradiance, ax, "year")
        fig.savefig(save_folder + plotname)
        plt.close(fig)

    df_parameter = dataframes.get("parameter", None)
    if df_parameter is not None:
        plotname = "total_parameterset.png"
        print(f"plotname: {plotname}")
        fig, ax = create_HKfig("FY-3 " + plotname + version)
        plot_parameter(df_parameter, ax)
        fig.savefig(save_folder + plotname)
        plt.close(fig)


parser = argparse.ArgumentParser(
    prog="DaraPlotter", description="Program to plot dara Data", epilog="Enjoy"
)
subparsers = parser.add_subparsers(help="mode", dest="command")
daily_parser = subparsers.add_parser("daily")
monthly_parser = subparsers.add_parser("monthly")
anual_parser = subparsers.add_parser("anual")
lifetime_parser = subparsers.add_parser("lifetime")
custom_parser = subparsers.add_parser("custom")

daily_parser.add_argument(
    "-sd", "--start_date", help="Startdate in format yyyy-mm-dd", type=str
)
daily_parser.add_argument(
    "-ed",
    "--end_date",
    help="Enddate in format yyyy-mm-dd",
    type=str,
    default=None,
)
daily_parser.add_argument(
    "-d",
    "--save_dir",
    help="Save directory for the plots",
    type=str,
    default="./plots/daily",
)

monthly_parser.add_argument(
    "-sm", "--start_month", help="Start Month in format: yyyy-mm", type=str
)
monthly_parser.add_argument(
    "-em",
    "--end_month",
    help="End Month in format: yyyy-mm",
    type=str,
    default=None,
)
monthly_parser.add_argument(
    "-d",
    "--save_dir",
    help="Save directory for the plots",
    type=str,
    default="./plots/daily",
)

anual_parser.add_argument(
    "-sy", "--start_year", help="Start Year in format: yyyy", type=str
)
anual_parser.add_argument(
    "-ey",
    "--end_year",
    help="End Year in format: yyyy",
    type=str,
    default=None,
)
anual_parser.add_argument(
    "-d",
    "--save_dir",
    help="Save directory for the plots",
    type=str,
    default="./plots/anual",
)

custom_parser.add_argument(
    "-sd", "--start_date", help="Startdate in format yyyy-mm-dd", type=str
)
custom_parser.add_argument(
    "-ed",
    "--end_date",
    help="Enddate in format yyyy-mm-dd",
    type=str,
    default=None,
)
custom_parser.add_argument(
    "-d",
    "--save_dir",
    help="Save directory for the plots",
    type=str,
    default="./plots/custom",
)

lifetime_parser.add_argument(
    "-d",
    "--save_dir",
    help="Save directory for the plots",
    type=str,
    default="./plots/lifetime",
)

# parser.add_argument('-m','--mode', help='Plot mode (daily, monthly, annual, lifetime or custom)')
# parser.add_argument('-sd', '--start_date', help='Startdate in format yyyy-mm-dd')
# parser.add_argument('-ed', '--end_date', help='Enddate in format yyyy-mm-dd')
# parser.print_help()
args = parser.parse_args()


def make_date_iterator(start_date, end_date, offset=None):
    if offset is None:
        yield start_date, end_date
        return
    lower_date = start_date
    upper_date = start_date + offset
    while upper_date <= end_date + offset:
        yield lower_date, upper_date
        lower_date = lower_date + offset
        upper_date = lower_date + offset
    # for
    # pass


if args.command == "daily":
    print(f"Plotten vom {args.start_date} bis zum {args.end_date}")
    start_date_arg = args.start_date
    end_date_arg = args.end_date
    if end_date_arg is None:
        end_date_arg = start_date_arg
    offset = pd.DateOffset(days=1)  # days or years
    mode = "day"

elif args.command == "monthly":
    print(f"Plotten vom {args.start_month} bis zum {args.end_month}")
    start_date_arg = args.start_month
    end_date_arg = args.end_month
    if end_date_arg is None:
        end_date_arg = start_date_arg
    offset = pd.DateOffset(months=1)  # days or years
    mode = "month"

elif args.command == "anual":
    print(f"Plotten vom {args.start_year} bis zum {args.end_year}")
    start_date_arg = args.start_year
    end_date_arg = args.end_year
    if end_date_arg is None:
        end_date_arg = start_date_arg
    offset = pd.DateOffset(years=1)  # days or years
    mode = "year"

elif args.command == "custom":
    print(f"Plotten vom {args.start_date} bis zum {args.end_date}")
    start_date_arg = args.start_date
    end_date_arg = args.end_date
    if end_date_arg is None:
        end_date_arg = start_date_arg
    offset = None
    mode = "custom"

elif args.command == "lifetime":
    pass

try:
    start_date = pd.to_datetime(start_date_arg)
    end_date = pd.to_datetime(end_date_arg)
except ValueError as e:
    print("Date Format could not be parsed")
    exit()
except pd.errors.ParserError as e:
    print("Date could not be parsed")
    exit()

conn_string = "mysql+mysqlconnector://dara_dev:password@localhost:3306/dara"
engine = create_engine(conn_string)

version = " / 0.1"
plotPostFix = f"{mode}.png"
# plotPostFix = f"RAD_Plot_{mode}.png"
save_folder = args.save_dir

if mode == "lifetime":
    irradiance_query = """SELECT 
        `timestamp`, `irradiance_a_wm2_`, `irradiance_b_wm2_`, `irradiance_c_wm2_`
        FROM irradiance
        WHERE timestamp is not null order by timestamp;"""
    df_irradiance = pd.read_sql(irradiance_query, con=engine)
    df_irradiance.columns = map(str.lower, df_irradiance.columns)
    print("Finish loading data from DB")
    print(f"Rows loaded {len(df_irradiance)}")

    parameter_query = """SELECT
        * FROM `parameterset` WHERE timestamp is not null"""
    df_parameter = pd.read_sql(parameter_query, con=engine)
    df_parameter.columns = map(str.lower, df_parameter.columns)
    print("Finish loading data from DB")
    print(f"Rows loaded {len(df_parameter)}")

    housekeeping_query = """
    SELECT * FROM housekeeping WHERE timestamp is not null;"""
    # and DATE_ADD('{end}', INTERVAL 1 DAY);"""

    calibration_query = """
    SELECT * FROM calibration WHERE timestamp is not null;"""
    print(housekeeping_query)
    print(calibration_query)

    df_housekeeping = pd.read_sql(housekeeping_query, con=engine)
    df_housekeeping.columns = map(str.lower, df_housekeeping.columns)
    print("Finish loading data from DB")
    print(f"Rows loaded {len(df_housekeeping)}")

    df_calibration = pd.read_sql(calibration_query, con=engine)
    df_calibration.columns = map(str.lower, df_calibration.columns)
    df_calibration = convert_cavity_to_numeric(df_calibration)
    print("Finish loading data from DB")
    print(f"Rows loaded {len(df_calibration)}")

    date_string = ""

    dataframes = {
        "housekeeping": df_housekeeping,
        "calibration": df_calibration,
        "parameter": df_parameter,
        "irradiance": df_irradiance,
    }
    make_plots(
        dataframes, date_string, plotPostFix, mode, version, save_folder
    )
    exit

for start, end in make_date_iterator(start_date, end_date, offset):
    housekeeping_query = f"""
    SELECT * FROM housekeeping WHERE timestamp 
    between '{start}' 
    and '{end}';"""
    # and DATE_ADD('{end}', INTERVAL 1 DAY);"""

    calibration_query = f"""
    SELECT * FROM calibration WHERE timestamp 
    between '{start}' 
    and '{end}';"""
    print(housekeeping_query)
    print(calibration_query)
    print(f"{start =}")
    print(f"{end =}")
    print("-" * 10)

    df_housekeeping = pd.read_sql(housekeeping_query, con=engine)
    df_housekeeping.columns = map(str.lower, df_housekeeping.columns)
    print("Finish loading data from DB")
    print(f"Rows loaded {len(df_housekeeping)}")

    df_calibration = pd.read_sql(calibration_query, con=engine)
    df_calibration.columns = map(str.lower, df_calibration.columns)
    df_calibration = convert_cavity_to_numeric(df_calibration)
    print("Finish loading data from DB")
    print(f"Rows loaded {len(df_calibration)}")

    date_string = ""
    if mode == "day" or mode == "custom":
        date_string = start.strftime("%Y-%m-%d")
    else:
        date_string = start.strftime("%Y-%m")

    dataframes = {
        "housekeeping": df_housekeeping,
        "calibration": df_calibration,
    }
    make_plots(
        dataframes, date_string, plotPostFix, mode, version, save_folder
    )

    # plotname = "_".join([date_string, "01_HK_Plot", plotPostFix])
    # print(f"plotname: {plotname}")
    # fig, ax = create_HKfig("FY-3 JTSIM DARA HK 1 " + date_string + version)
    # plot_HK_1(df_housekeeping, ax, mode)
    # fig.savefig(save_folder + "/" + plotname)
    # plt.close(fig)
#
# plotname = "_".join([date_string, "02_HK_Plot", plotPostFix])
# print(f"plotname: {plotname}")
# fig, ax = create_HKfig("FY-3 JTSIM DARA HK 2 " + date_string + version)
# plot_HK_2(df_housekeeping, ax, mode)
# fig.savefig(save_folder + "/" + plotname)
# plt.close(fig)
#
# plotname = "_".join([date_string, "RAD_Plot", plotPostFix])
# print(f"plotname: {plotname}")
# fig, ax = create_Irradfig("FY-3 JTSIM DARA RAD " + date_string + version)
# plot_SCI_1(df_calibration, ax, mode)
# fig.savefig(save_folder + "/" + plotname)
# plt.close(fig)
#
