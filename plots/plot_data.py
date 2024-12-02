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


def date_iterator(start_date, end_date, offset=None):
    if offset is None:
        yield start_date, end_date
        return
    lower_date = start_date
    upper_date = start_date + offset
    while upper_date <= end_date + offset:
        yield lower_date, upper_date
        lower_date = lower_date + offset
        upper_date = lower_date + offset

def make_plots(
    dataframes, date_string, plotPostFix, mode, version, save_folder
):
    df_housekeeping = dataframes["housekeeping"]

    plotname = "_".join(filter(None,[date_string, "01_HK_Plot", plotPostFix]))
    print(f"plotting {plotname}")
    fig, ax = create_HKfig("FY-3 JTSIM DARA HK 1 " + date_string + version)
    plot_HK_1(df_housekeeping, ax, mode)
    fig.savefig(save_folder + "/" + plotname)
    plt.close(fig)

    plotname = "_".join(filter(None,[date_string, "02_HK_Plot", plotPostFix]))
    print(f"plotting {plotname}")
    fig, ax = create_HKfig("FY-3 JTSIM DARA HK 2 " + date_string + version)
    plot_HK_2(df_housekeeping, ax, mode)
    fig.savefig(save_folder + "/" + plotname)
    plt.close(fig)

    df_calibration = dataframes["calibration"]

    plotname = "_".join(filter(None,[date_string, "RAD_Plot", plotPostFix]))
    print(f"plotting {plotname}")
    fig, ax = create_Irradfig("FY-3 JTSIM DARA RAD " + date_string + version)
    plot_SCI_1(df_calibration, ax, mode)
    fig.savefig(save_folder + "/" + plotname)
    plt.close(fig)

    df_irradiance = dataframes.get("irradiance", None)
    if df_irradiance is not None:
        plotname = "_".join(filter(None,[date_string, "irradiance", plotPostFix]))
        # plotname = "total_irradiance.png"
        print(f"plotting {plotname}")
        fig, ax = create_irradiance_fig(
            "FY-3 JTSIM DARA Irradiance " + plotname + version
        )
        plot_irr(df_irradiance, ax, mode)
        fig.savefig(save_folder + '/' +  plotname)
        plt.close(fig)

    df_parameter = dataframes.get("parameter", None)
    if df_parameter is not None:
        plotname = "_".join(filter(None,[date_string, "parameterset", plotPostFix]))
        # plotname = "total_parameterset.png"
        print(f"plotting {plotname}")
        fig, ax = create_HKfig("FY-3 " + plotname + version)
        plot_parameter(df_parameter, ax)
        fig.savefig(save_folder + '/' +  plotname)
        plt.close(fig)

def main(args):
    conn_string = "mysql+mysqlconnector://dara_dev:password@localhost:3306/dara"
    engine = create_engine(conn_string)

    if args.command == "daily":
        start_date_arg = args.start_date
        end_date_arg = args.end_date
        if end_date_arg is None:
            end_date_arg = start_date_arg
        offset = pd.DateOffset(days=1)
        mode = "daily"

    elif args.command == "monthly":
        start_date_arg = args.start_month
        end_date_arg = args.end_month
        if end_date_arg is None:
            end_date_arg = start_date_arg
        offset = pd.DateOffset(months=1)
        mode = "monthly"

    elif args.command == "anual":
        start_date_arg = args.start_year
        end_date_arg = args.end_year
        if end_date_arg is None:
            end_date_arg = start_date_arg
        offset = pd.DateOffset(years=1)
        mode = "anual"

    elif args.command == "custom":
        start_date_arg = args.start_date
        end_date_arg = args.end_date
        if end_date_arg is None:
            end_date_arg = start_date_arg
        offset = None
        mode = "custom"

    elif args.command == "lifetime":
        mode='lifetime'
        pass

    if mode != 'lifetime':
        try:
            start_date = pd.to_datetime(start_date_arg)
            end_date = pd.to_datetime(end_date_arg)
        except ValueError as e:
            print("Date Format could not be parsed")
            exit()
        except pd.errors.ParserError as e:
            print("Date could not be parsed")
            exit()

    version = " / 0.1"
    plotPostFix = f"{mode}.png"
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
        SELECT * FROM housekeeping WHERE timestamp is not null ORDER BY timestamp;"""
        # and DATE_ADD('{end}', INTERVAL 1 DAY);"""

        calibration_query = """
        SELECT * FROM calibration WHERE timestamp is not null ORDER BY timestamp;"""
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
        return

    for start, end in date_iterator(start_date, end_date, offset):
        print('')
        print(f'Plot between {start} and {end}')
        housekeeping_query = f"""
        SELECT * FROM housekeeping WHERE timestamp 
        between '{start}' 
        and '{end}'
        ORDER BY timestamp;"""

        calibration_query = f"""
        SELECT * FROM calibration WHERE timestamp 
        between '{start}' 
        and '{end}'
        ORDER BY timestamp;"""

        print('Loading from Housekeeping ...')
        df_housekeeping = pd.read_sql(housekeeping_query, con=engine)
        df_housekeeping.columns = map(str.lower, df_housekeeping.columns)
        print(f"Rows loaded {len(df_housekeeping)}")

        print('Loading from Calibration ...')
        df_calibration = pd.read_sql(calibration_query, con=engine)
        df_calibration.columns = map(str.lower, df_calibration.columns)
        df_calibration = convert_cavity_to_numeric(df_calibration)
        print(f"Rows loaded {len(df_calibration)}")

        date_string = ""
        if mode == "daily":
            date_string = start.strftime("%Y-%m-%d")
        elif mode == 'custom':
            date_string = '_'.join([start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")])
        else:
            date_string = start.strftime("%Y-%m")
        
        dataframes = {
            "housekeeping": df_housekeeping,
            "calibration": df_calibration,
        }

        if args.add_irradiance:
            irradiance_query = f"""SELECT 
                `timestamp`, `irradiance_a_wm2_`, `irradiance_b_wm2_`, `irradiance_c_wm2_`
                FROM irradiance
                WHERE timestamp
                between '{start}' 
                and '{end}'
                order by timestamp;"""
            print('Loading from Irradiance ...')
            df_irradiance = pd.read_sql(irradiance_query, con=engine)
            df_irradiance.columns = map(str.lower, df_irradiance.columns)
            print(f"Rows loaded {len(df_irradiance)}")
            dataframes['irradiance'] = df_irradiance

        make_plots(
            dataframes, date_string, plotPostFix, mode, version, save_folder
        )

if __name__ == '__main__':
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
        "-s", "--start_date", help="Startdate in format yyyy-mm-dd", type=str
    )
    daily_parser.add_argument(
        "-e",
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
    daily_parser.add_argument('--add_irradiance', action='store_true', default=False)

    monthly_parser.add_argument(
        "-s", "--start_month", help="Start Month in format: yyyy-mm", type=str
    )
    monthly_parser.add_argument(
        "-e",
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
    monthly_parser.add_argument('--add_irradiance', action='store_true', default=False)

    anual_parser.add_argument(
        "-s", "--start_year", help="Start Year in format: yyyy", type=str
    )
    anual_parser.add_argument(
        "-e",
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
    anual_parser.add_argument('--add_irradiance', action='store_true', default=False)

    custom_parser.add_argument(
        "-s", "--start_date", help="Startdate in format yyyy-mm-dd", type=str
    )
    custom_parser.add_argument(
        "-e",
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
    custom_parser.add_argument('--add_irradiance', action='store_true', default=False)

    lifetime_parser.add_argument(
        "-d",
        "--save_dir",
        help="Save directory for the plots",
        type=str,
        default="./plots/lifetime",
    )

    # parser.add_argument(
        # "-c",
        # "--connection_string",
        # help="BlaBliBlaBlu",
        # type=str,
        # default="mysql+mysqlconnector://dara_dev:password@localhost:3306/dara",
    # )
# 
    args = parser.parse_args()
    main(args)
