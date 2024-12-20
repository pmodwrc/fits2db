#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Libuaries USED:
    matplotlib.pyplot
    astropy.io.fitsprint(valTime.format)
    astropy.time
    pathlib
    pandas

MODIFICATION HISTORY:
      Created on Fri Dec  8 11:29:12 2017

       @author: manfred.gyo
       adapted for JTSIM DARA by Dany Pfiffner December 2019 Lijiang
       adapted for DARA by Dany Pfiffner 2020 Jan 29.
       reworked for JTSIM DARA by Dany Pfiffner August 2021

"""

import datetime
from matplotlib import ticker
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from matplotlib.ticker import AutoMinorLocator, MultipleLocator


def replace(i):
    switcher = {"none": 0, "A": 1, "B": 2, "C": 3}
    return switcher.get(i, 0)


def create_HKfig(plotTitle):
    # set plot defaults
    plt.rcParams["figure.titlesize"] = 12
    plt.rcParams["figure.titleweight"] = "bold"
    plt.rcParams["figure.subplot.hspace"] = 0.35
    plt.rcParams["font.size"] = 8
    plt.rcParams["lines.linewidth"] = 1
    plt.rcParams["lines.markersize"] = 5
    plt.rcParams["legend.fontsize"] = 6
    plt.rcParams["legend.loc"] = "best"
    plt.rcParams["legend.numpoints"] = 10
    plt.rcParams["axes.grid"] = "True"
    plt.rcParams["axes.grid.axis"] = "both"
    plt.rcParams["axes.labelsize"] = 8
    plt.rcParams["axes.linewidth"] = 0.8
    plt.rcParams["axes.titlesize"] = 8
    plt.rcParams["savefig.dpi"] = 500

    f, ax = plt.subplots(3, 2, figsize=(9, 11), layout="constrained")
    f.suptitle(plotTitle + "\n ", fontsize=12, fontweight="bold")
    f.dpi = 500
    return f, ax


def create_Irradfig(plotTitle):
    # set plot defaults
    plt.rcParams["figure.titlesize"] = 12
    plt.rcParams["figure.titleweight"] = "bold"
    plt.rcParams["figure.subplot.hspace"] = 0.35
    plt.rcParams["font.size"] = 8
    plt.rcParams["lines.linewidth"] = 1
    plt.rcParams["lines.markersize"] = 5
    plt.rcParams["legend.fontsize"] = 6
    plt.rcParams["legend.loc"] = "best"
    plt.rcParams["legend.numpoints"] = 10
    plt.rcParams["axes.grid"] = "True"
    plt.rcParams["axes.grid.axis"] = "both"
    plt.rcParams["axes.labelsize"] = 8
    plt.rcParams["axes.linewidth"] = 0.8
    plt.rcParams["axes.titlesize"] = 8
    plt.rcParams["savefig.dpi"] = 500

    f, ax = plt.subplots(3, 2, figsize=(9, 11), layout="constrained")
    f.suptitle(plotTitle + "\n ", fontsize=12, fontweight="bold")
    f.dpi = 500
    return f, ax


def create_irradiance_fig(plot_title):
    # set plot defaults
    plt.rcParams["figure.titlesize"] = 12
    plt.rcParams["figure.titleweight"] = "bold"
    plt.rcParams["figure.subplot.hspace"] = 0.35
    plt.rcParams["font.size"] = 8
    plt.rcParams["lines.linewidth"] = 1
    plt.rcParams["lines.markersize"] = 5
    plt.rcParams["legend.fontsize"] = 6
    plt.rcParams["legend.loc"] = "best"
    plt.rcParams["legend.numpoints"] = 10
    plt.rcParams["axes.grid"] = "True"
    plt.rcParams["axes.grid.axis"] = "both"
    plt.rcParams["axes.labelsize"] = 8
    plt.rcParams["axes.linewidth"] = 0.8
    plt.rcParams["axes.titlesize"] = 8
    plt.rcParams["savefig.dpi"] = 500

    f, ax = plt.subplots(3, 1, figsize=(9, 11), layout="constrained")
    f.suptitle(plot_title + "\n", fontsize=12, fontweight="bold")
    f.dpi = 500
    return f, ax


def convert_cavity_to_numeric(
    df,
):
    cavity_map = {
        "a": 1,
        "A": 1,
        "b": 2,
        "B": 2,
        "c": 3,
        "C": 3,
        "none": 0,
        None: 0,
    }
    df["nominal_cavity"] = (
        df["nominal_cavity"]
        .map(lambda x: cavity_map.get(x, 0))
        .astype("uint8")
    )
    df["reference_cavity"] = (
        df["reference_cavity"]
        .map(lambda x: cavity_map.get(x, 0))
        .astype("uint8")
    )
    df["backup_cavity_1"] = (
        df["backup_cavity_1"]
        .map(lambda x: cavity_map.get(x, 0))
        .astype("uint8")
    )
    return df
    pass


def plot_HK_1_from_cfg(hkdata: pd.DataFrame, ax: plt.Axes, mode: str, cfg):
    __ms = 0.5
    if mode == "day" or mode == "daily":
        for a in ax.flat:
            a.set_xlabel("Time UTC")
            a.xaxis.set_major_locator(
                mdates.HourLocator(interval=4)
            )  # Set major ticks every 4 hours
            a.xaxis.set_major_formatter(mdates.DateFormatter("%Hh"))
            start_time = mdates.date2num(hkdata["timestamp"].min())
            # end_time = mdates.date2num(hkdata["timestamp"].max())
            end_time = start_time + 1
            a.set_xlim(start_time, end_time)
            a.grid(True)
            a.tick_params(axis="x", rotation=30)
            # labels = a.get_xticklabels()
            # for label in labels:
            # label.update({'horizontalalignment': 'right'})

    for subplot in cfg["content"]:
        axis = ax[subplot["row"], subplot["col"]]
        axis.set_title(subplot["title"])
        axis.set_ylabel(subplot["ylabel"])
        offset = subplot["y_offset"]
        for plot_cfg in subplot["data"]:
            axis.plot(
                hkdata[plot_cfg["x"]],
                hkdata[plot_cfg["y"]] + offset,
                plot_cfg["marker"],
                color=plot_cfg["color"],
                markersize=__ms,
                label=plot_cfg["label"],
            )
        ylims = subplot.get("ylims", None)
        if ylims is not None:
            axis.set_ylim(tuple(ylims))
        axis.legend(
            numpoints=5,
            ncol=2,
            loc=subplot["legend_loc"],
        )


def plot_HK_1(hkdata: pd.DataFrame, ax: plt.Axes, mode: str):
    __ms = 0.5

    if mode == "day" or mode == "daily":
        for a in ax.flat:
            a.set_xlabel("Time UTC")
            a.xaxis.set_major_locator(
                mdates.HourLocator(interval=4)
            )  # Set major ticks every 4 hours
            a.xaxis.set_major_formatter(mdates.DateFormatter("%Hh"))
            start_time = mdates.date2num(hkdata["timestamp"].min())
            # end_time = mdates.date2num(hkdata["timestamp"].max())
            end_time = start_time + 1
            a.set_xlim(start_time, end_time)

    if mode == "month" or mode == "monthly":
        for a in ax.flat:
            a.set_xlabel("Date UTC")
            # a.xaxis.set_major_locator(
            # mdates.DayLocator(bymonthday=range(1,32), interval=3)
            # )  # Set major ticks every 3 Days
            a.set_xticks(
                mdates.drange(
                    hkdata["timestamp"].min().date(),
                    hkdata["timestamp"].max().date() + datetime.timedelta(1),
                    datetime.timedelta(3),
                )
            )
            a.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y"))
            start_time = mdates.date2num(hkdata["timestamp"].min().date())
            end_time = mdates.date2num(hkdata["timestamp"].max().date())
            a.set_xlim(left=start_time, right=end_time + 1)

    if mode == "year" or mode == "anual":
        for a in ax.flat:
            a.set_xlabel("Date UTC")
            a.xaxis.set_major_locator(
                mdates.MonthLocator()
            )  # Set major ticks every 3 Days
            a.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y"))

    if mode == "lifetime":
        for a in ax.flat:
            a.set_xlabel("Date UTC")
            a.xaxis.set_major_locator(
                mdates.MonthLocator(interval=3)
            )  # Set major ticks every 3 Days
            a.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y"))

    if mode == "custom":
        for a in ax.flat:
            a.set_xlabel("Date UTC")
            a.xaxis.set_major_locator(plt.MaxNLocator(12))
            a.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y"))

    for a in ax.flat:
        a.grid(True)
        a.tick_params(axis="x", rotation=30)
        # Uncomment for different xticklabels alignment
        # labels = a.get_xticklabels()
        # for label in labels:
        # label.update({'horizontalalignment': 'right'})

    ax[0, 0].set_title("DCDC Temperatures")
    ax[0, 0].set_ylabel("Temp [°C]")
    ax[0, 0].plot(
        hkdata["timestamp"],
        hkdata["dcdc_12vdcdc_temp"] - 273.15,
        "o",
        color="blue",
        markersize=__ms,
        label="DCDC_12VDCDC_Temp",
    )
    ax[0, 0].plot(
        hkdata["timestamp"],
        hkdata["dcdc_5vdcdc_temp"] - 273.15,
        "o",
        color="red",
        markersize=__ms,
        label="DCDC_5VDCDC_Temp",
    )
    ax[0, 0].plot(
        hkdata["timestamp"],
        hkdata["dcdc_icl_temp"] - 273.15,
        "o",
        color="green",
        markersize=__ms,
        label="DCDC_ICL_Temp",
    )
    ax[0, 0].plot(
        hkdata["timestamp"],
        hkdata["dcdc_cs_temp"] - 273.15,
        "o",
        color="cyan",
        markersize=__ms,
        label="DCDC_CS_Temp",
    )
    ax[0, 0].set_ylim(-20, 50)
    ax[0, 0].legend(
        numpoints=5,
        ncol=2,
        loc="upper right",
    )

    ax[0, 1].set_title("Currents")
    ax[0, 1].set_ylabel("Current [mA]")
    ax[0, 1].plot(
        hkdata["timestamp"],
        hkdata["dcdc_5vpos_d_cm"],
        "o",
        color="blue",
        markersize=__ms,
        label="DCDC_5VPOS_D_CM",
    )
    ax[0, 1].plot(
        hkdata["timestamp"],
        hkdata["dcdc_5vpos_a_cm"],
        "o",
        color="red",
        markersize=__ms,
        label="DCDC_5VPOS_A_CM",
    )
    ax[0, 1].plot(
        hkdata["timestamp"],
        hkdata["dcdc_12vpos_cm"],
        "o",
        color="green",
        markersize=__ms,
        label="DCDC_12VPOS_CM",
    )
    ax[0, 1].plot(
        hkdata["timestamp"],
        hkdata["dcdc_12vneg_cm"],
        "o",
        color="cyan",
        markersize=__ms,
        label="DCDC_12VNEG_CM",
    )
    ax[0, 1].plot(
        hkdata["timestamp"],
        hkdata["dcdc_28v_prim_current"],
        "o",
        color="magenta",
        markersize=__ms,
        label="DCDC_28V_PRIM_CURRENT",
    )
    # ax[0,1].plot(hkdata['timestamp'], hkdata['CPU_5VCPU_CM'],color='yellow',markersize=__ms)
    ax[0, 1].set_ylim(-0.1, 0.9)
    ax[0, 1].legend(
        numpoints=5,
        ncol=2,
        loc="upper right",
    )

    ax[1, 0].set_title("CPU Temperatures")
    ax[1, 0].set_ylabel("Temp [°C]")
    ax[1, 0].plot(
        hkdata["timestamp"],
        hkdata["cpu_hkref_temp"] - 273.15,
        "o",
        color="blue",
        markersize=__ms,
        label="CPU_HKREF_TEMP",
    )
    ax[1, 0].plot(
        hkdata["timestamp"],
        hkdata["cpu_adc_temp"] - 273.15,
        "o",
        color="red",
        markersize=__ms,
        label="CPU_ADC_TEMP",
    )
    ax[1, 0].plot(
        hkdata["timestamp"],
        hkdata["cpu_cpu_temp"] - 273.15,
        "o",
        color="green",
        markersize=__ms,
        label="CPU_CPU_TEMP",
    )
    ax[1, 0].plot(
        hkdata["timestamp"],
        hkdata["cpu_mram_temp"] - 273.15,
        "o",
        color="cyan",
        markersize=__ms,
        label="CPU_MRAM_TEMP",
    )
    ax[1, 0].plot(
        hkdata["timestamp"],
        hkdata["cpu_sram_temp"] - 273.15,
        "o",
        color="magenta",
        markersize=__ms,
        label="CPU_SRAM_TEMP",
    )
    ax[1, 0].plot(
        hkdata["timestamp"],
        hkdata["cpu_osc_temp"] - 273.15,
        "o",
        color="yellow",
        markersize=__ms,
        label="CPU_OSC_TEMP",
    )
    # ax[1,0].plot(hkdata['timestamp'], hkdata['CPU_SIN_TEMP')-273.15,color='pink',markersize=__ms)
    ax[1, 0].set_ylim(-20, 50)

    ax[1, 0].legend(
        numpoints=5,
        ncol=2,
        loc="lower right",
    )

    # plot Secondary Voltages graph
    ax[1, 1].set_title("Secondary Voltages")
    ax[1, 1].set_ylabel("Voltage [V]")
    ax[1, 1].plot(
        hkdata["timestamp"],
        hkdata["dcdc_5vpos_a_prot"],
        "o",
        color="blue",
        markersize=__ms,
        label="DCDC_5VPOS_A_PROT",
    )
    ax[1, 1].plot(
        hkdata["timestamp"],
        hkdata["dcdc_5vpos_d_prot"],
        "o",
        color="red",
        markersize=__ms,
        label="DCDC_5VPOS_D_PROT",
    )
    ax[1, 1].plot(
        hkdata["timestamp"],
        hkdata["dcdc_12vneg_prot"],
        "o",
        color="green",
        markersize=__ms,
        label="DCDC_12VNEG_PROT",
    )
    ax[1, 1].plot(
        hkdata["timestamp"],
        hkdata["dcdc_12vpos_prot"],
        "o",
        color="cyan",
        markersize=__ms,
        label="DCDC_12VPOS_PROT",
    )

    ax[1, 1].plot(
        hkdata["timestamp"],
        hkdata["cpu_vcc"],
        "o",
        color="yellow",
        markersize=__ms,
        label="CPU_VCC",
    )
    ax[1, 1].plot(
        hkdata["timestamp"],
        hkdata["cpu_vcc_3v3"],
        "o",
        color="pink",
        markersize=__ms,
        label="CPU_VCC_3V3",
    )
    ax[1, 1].set_ylim(-12.5, 22)

    ax[1, 1].legend(
        numpoints=5,
        ncol=2,
        loc="upper right",
    )

    # plot 4Q Sensor graph
    ax[2, 0].set_title("DAQ Temperatures")
    ax[2, 0].set_ylabel("Temp [°C]")
    ax[2, 0].plot(
        hkdata["timestamp"],
        hkdata["daq_inst_a_i_temp"] - 273.15,
        "o",
        color="blue",
        markersize=__ms,
        label="DAQ_INST_A_I_TEMP",
    )
    ax[2, 0].plot(
        hkdata["timestamp"],
        hkdata["daq_inst_b_i_temp"] - 273.15,
        "o",
        color="red",
        markersize=__ms,
        label="DAQ_INST_B_I_TEMP",
    )
    ax[2, 0].plot(
        hkdata["timestamp"],
        hkdata["daq_inst_c_i_temp"] - 273.15,
        "o",
        color="green",
        markersize=__ms,
        label="DAQ_INST_C_I_TEMP",
    )
    ax[2, 0].plot(
        hkdata["timestamp"],
        hkdata["daq_ref_temp"] - 273.15,
        "o",
        color="cyan",
        markersize=__ms,
        label="DAQ_REF_TEMP",
    )
    ax[2, 0].plot(
        hkdata["timestamp"],
        hkdata["daq_a_temp"] - 273.15,
        "o",
        color="magenta",
        markersize=__ms,
        label="DAQ_A_TEMP",
    )
    ax[2, 0].plot(
        hkdata["timestamp"],
        hkdata["daq_b_temp"] - 273.15,
        "o",
        color="yellow",
        markersize=__ms,
        label="DAQ_B_TEMP",
    )
    ax[2, 0].plot(
        hkdata["timestamp"],
        hkdata["daq_c_temp"] - 273.15,
        "o",
        color="pink",
        markersize=__ms,
        label="DAQ_C_TEMP",
    )
    ax[2, 0].plot(
        hkdata["timestamp"],
        hkdata["daq_d_temp"] - 273.15,
        "o",
        color="purple",
        markersize=__ms,
        label="DAQ_D_TEMP",
    )
    ax[2, 0].plot(
        hkdata["timestamp"],
        hkdata["daq_e_temp"] - 273.15,
        "o",
        color="orange",
        markersize=__ms,
        label="DAQ_E_TEMP",
    )
    ax[2, 0].set_ylim(-20, 50)

    ax[2, 0].legend(
        numpoints=5,
        ncol=2,
        loc="lower left",
    )

    # plot Reference Volatges graph
    ax[2, 1].set_title("Shutter Board Temperatures")
    ax[2, 1].set_ylabel("TEMP [°C]")
    ax[2, 1].plot(
        hkdata["timestamp"],
        hkdata["sb_sha_board_temp"] - 273.15,
        "o",
        color="blue",
        markersize=__ms,
        label="SB_SHA_BOARD_TEMP",
    )
    ax[2, 1].plot(
        hkdata["timestamp"],
        hkdata["sb_shb_board_temp"] - 273.15,
        "o",
        color="red",
        markersize=__ms,
        label="SB_SHB_BOARD_TEMP",
    )
    ax[2, 1].plot(
        hkdata["timestamp"],
        hkdata["sb_shc_board_temp"] - 273.15,
        "o",
        color="green",
        markersize=__ms,
        label="SB_SHC_BOARD_TEMP",
    )
    ax[2, 1].plot(
        hkdata["timestamp"],
        hkdata["sb_mot_a_temp"] - 273.15,
        "o",
        color="cyan",
        markersize=__ms,
        label="SB_MOT_A_TEMP",
    )
    ax[2, 1].plot(
        hkdata["timestamp"],
        hkdata["sb_mot_b_temp"] - 273.15,
        "o",
        color="magenta",
        markersize=__ms,
        label="SB_MOT_B_TEMP",
    )
    ax[2, 1].plot(
        hkdata["timestamp"],
        hkdata["sb_mot_c_temp"] - 273.15,
        "o",
        color="yellow",
        markersize=__ms,
        label="SB_MOT_C_TEMP",
    )
    ax[2, 1].plot(
        hkdata["timestamp"],
        hkdata["sb_reg_a_temp"] - 273.15,
        "o",
        color="pink",
        markersize=__ms,
        label="SB_REG_A_TEMP",
    )
    ax[2, 1].plot(
        hkdata["timestamp"],
        hkdata["sb_reg_b_temp"] - 273.15,
        "o",
        color="purple",
        markersize=__ms,
        label="SB_REG_B_TEMP",
    )
    ax[2, 1].plot(
        hkdata["timestamp"],
        hkdata["sb_reg_c_temp"] - 273.15,
        "o",
        color="orange",
        markersize=__ms,
        label="SB_REG_C_TEMP",
    )
    ax[2, 1].plot(
        hkdata["timestamp"],
        hkdata["sb_mcu_temp"] - 273.15,
        "o",
        color="lightblue",
        markersize=__ms,
        label="SB_MCU_TEMP",
    )
    ax[2, 1].plot(
        hkdata["timestamp"],
        hkdata["sb_case_temp"] - 273.15,
        "o",
        color="lightgreen",
        markersize=__ms,
        label="SB_CASE_TEMP",
    )
    ax[2, 1].plot(
        hkdata["timestamp"],
        hkdata["sb_bottom_temp"] - 273.15,
        "o",
        color="grey",
        markersize=__ms,
        label="SB_BOTTOM_TEMP",
    )
    ax[2, 1].set_ylim(-20, 50)
    ax[2, 1].legend(
        numpoints=5,
        ncol=2,
        loc="upper right",
    )


def plot_HK_2(hkdata: pd.DataFrame, ax: plt.Axes, mode: str):
    __ms = 0.5

    if mode == "day" or mode == "daily":
        for a in ax[:-1].flat:
            a.set_xlabel("Time UTC")
            a.xaxis.set_major_locator(
                mdates.HourLocator(interval=4)
            )  # Set major ticks every 4 hours
            a.xaxis.set_major_formatter(mdates.DateFormatter("%Hh"))
            start_time = mdates.date2num(hkdata["timestamp"].min())
            end_time = start_time + 1
            a.set_xlim(start_time, end_time)

    if mode == "month" or mode == "monthly":
        for a in ax[:-1].flat:
            a.set_xlabel("Date UTC")
            # a.xaxis.set_major_locator(
            #     mdates.DayLocator(bymonthday=range(1, 32, 3), interval=3)
            # )  # Set major ticks every 3 Days
            a.set_xticks(
                mdates.drange(
                    hkdata["timestamp"].min().date(),
                    hkdata["timestamp"].max().date() + datetime.timedelta(1),
                    datetime.timedelta(3),
                )
            )
            a.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y"))

            start_time = mdates.date2num(hkdata["timestamp"].min().date())
            end_time = mdates.date2num(hkdata["timestamp"].max().date())
            a.set_xlim(left=start_time, right=end_time + 1)

    if mode == "year" or mode == "anual":
        for a in ax[:-1].flat:
            a.set_xlabel("Date UTC")
            a.xaxis.set_major_locator(
                mdates.MonthLocator()
            )  # Set major ticks every 3 Days
            # a.xaxis.set_major_locator(mdates.YearLocator())
            a.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y"))

    if mode == "lifetime":
        for a in ax[:-1].flat:
            a.set_xlabel("Date UTC")
            a.xaxis.set_major_locator(
                mdates.MonthLocator(interval=3)
            )  # Set major ticks every 3 Days
            # a.xaxis.set_major_locator(mdates.YearLocator())
            a.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y"))

    if mode == "custom":
        for a in ax.flat:
            a.set_xlabel("Date UTC")
            a.xaxis.set_major_locator(plt.MaxNLocator(12))
            a.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y"))

    for a in ax.flat:
        a.grid(True)
        a.tick_params(axis="x", rotation=30)
        # labels = a.get_xticklabels()
        # for label in labels:
        # label.update({'horizontalalignment': 'right'})

    ax[0, 0].set_title("Cavity Temperatures")
    ax[0, 0].set_ylabel("Temp [°C]")
    ax[0, 0].plot(
        hkdata["timestamp"],
        hkdata["cav_heatsink_temp"] - 273.15,
        "o",
        color="blue",
        markersize=__ms,
        label="CAV_HEATSINK_TEMP",
    )
    ax[0, 0].plot(
        hkdata["timestamp"],
        hkdata["cav_inst_a_u_temp"] - 273.15,
        "o",
        color="red",
        markersize=__ms,
        label="CAV_INST_A_U_TEMP",
    )
    ax[0, 0].plot(
        hkdata["timestamp"],
        hkdata["cav_inst_b_u_temp"] - 273.15,
        "o",
        color="green",
        markersize=__ms,
        label="CAV_INST_B_U_TEMP",
    )
    ax[0, 0].plot(
        hkdata["timestamp"],
        hkdata["cav_inst_c_u_temp"] - 273.15,
        "o",
        color="cyan",
        markersize=__ms,
        label="CAV_INST_C_U_TEMP",
    )
    ax[0, 0].set_ylim(-20, 50)
    ax[0, 0].legend(
        numpoints=5,
        ncol=2,
        loc="upper right",
    )

    ax[0, 1].set_title("4Q Sensor Raw")
    ax[0, 1].set_ylabel("Voltage [V]")

    ax[0, 1].plot(
        hkdata["timestamp"],
        hkdata["sb_4qa"],
        "o",
        color="blue",
        markersize=__ms,
        label="SB_4QA",
    )
    ax[0, 1].plot(
        hkdata["timestamp"],
        hkdata["sb_4qb"],
        "o",
        color="red",
        markersize=__ms,
        label="SB_4QB",
    )
    ax[0, 1].plot(
        hkdata["timestamp"],
        hkdata["sb_4qc"],
        "o",
        color="green",
        markersize=__ms,
        label="SB_4QC",
    )
    ax[0, 1].plot(
        hkdata["timestamp"],
        hkdata["sb_4qd"],
        "o",
        color="cyan",
        markersize=__ms,
        label="SB_4QD",
    )
    ax[0, 1].plot(
        hkdata["timestamp"],
        hkdata["sb_4qa"]
        + hkdata["sb_4qb"]
        + hkdata["sb_4qc"]
        + hkdata["sb_4qd"],
        "o",
        color="magenta",
        markersize=__ms,
        label="sum",
    )

    # ax[0,1].plot(hkdata['timestamp'], hkdata['CPU_5VCPU_CM'),color='yellow',markersize=__ms)
    ax[0, 1].set_ylim(-0.1, 1.5)
    ax[0, 1].legend(
        numpoints=5,
        ncol=2,
        loc="upper right",
    )

    # Beta Angle Calculation:  ((4QB+4QC)-(4QD+4QA))/(4QA+4QB+4QC+4QD)
    # Gamma Angle Calculation: ((4QC+4QD)-(4QB+4QA))/(4QA+4QB+4QC+4QD)

    __sum = (
        hkdata["sb_4qc"]
        + hkdata["sb_4qd"]
        + hkdata["sb_4qb"]
        + hkdata["sb_4qa"]
    )
    __beta = (
        hkdata["sb_4qc"]
        + hkdata["sb_4qb"]
        - hkdata["sb_4qd"]
        - hkdata["sb_4qa"]
    ) / __sum
    __gamma = (
        hkdata["sb_4qc"]
        + hkdata["sb_4qd"]
        - hkdata["sb_4qb"]
        - hkdata["sb_4qa"]
    ) / __sum

    # # JTSIM DARA
    ___beta = (
        0.6174 * __beta**3 + 0.0248 * __beta**2 + 1.1688 * __beta + 0.9838
    ) * 60
    ___gamma = (
        0.4936 * __gamma**3 - 0.0405 * __gamma**2 + 1.2281 * __gamma + 0.6233
    ) * 60

    for i in range(len(__sum)):
        try:
            if (
                __sum[__sum.index[i]] <= 0.8
            ):  # treshold level: if sum is smaller then 0.8V set sum gamma and beta value to 0.0
                __sum[__sum.index[i]] = 0.0
                ___beta[___beta.index[i]] = 0.0
                ___gamma[___gamma.index[i]] = 0.0
        except:
            print("shity error")

    ax[1, 0].set_title("4Q Sensor Eval")
    ax[1, 0].set_ylabel("arcmin")
    # ax[1, 0].plot(hkdata["timestamp"], ___gamma, "b", markersize=__ms)
    # ax[1, 0].plot(hkdata["timestamp"], ___beta, "r", markersize=__ms)
    ax[1, 0].plot(
        hkdata["timestamp"], ___gamma, "b.", markersize=__ms, label="GAMMA"
    )
    ax[1, 0].plot(
        hkdata["timestamp"], ___beta, "r.", markersize=__ms, label="BETA"
    )
    ax[1, 0].set_ylim(-60, 60)
    ax[1, 0].legend(numpoints=5, ncol=2, loc="upper right")

    # plot Auxilliary Voltages graph
    ax[1, 1].set_title("Aux Voltages")
    ax[1, 1].set_ylabel("Voltage [V]")
    ax[1, 1].plot(
        hkdata["timestamp"],
        hkdata["daq_hk_ref_mon"],
        "o",
        color="blue",
        markersize=__ms,
        label="DAQ_HK_REF_MON",
    )
    ax[1, 1].plot(
        hkdata["timestamp"],
        hkdata["adc128s_5v"],
        "o",
        color="red",
        markersize=__ms,
        label="ADC128S_5V",
    )
    ax[1, 1].plot(
        hkdata["timestamp"],
        hkdata["adc128s_2v5"],
        "o",
        color="green",
        markersize=__ms,
        label="ADC128S_2V5",
    )
    ax[1, 1].plot(
        hkdata["timestamp"],
        hkdata["adc128s_agnd"],
        "o",
        color="cyan",
        markersize=__ms,
        label="ADC128S_AGND",
    )
    ax[1, 1].set_ylim(-0.1, 6)
    ax[1, 1].legend(
        numpoints=5,
        ncol=2,
        loc="upper right",
    )

    # plot 4Q Sensor graph
    circle1 = plt.Circle((0, 0), 45, color="blue", fill=False)
    # circle1 = plt.Circle((0, 0), 45, color="gray", fill=True)
    ax[2, 0].xaxis.set_major_locator(MultipleLocator(20))
    ax[2, 0].xaxis.set_major_formatter("{x:.0f}")
    ax[2, 0].add_patch(circle1)
    ax[2, 0].set_title("4Q Sensor Eval")
    ax[2, 0].set_xlabel("arcmin GAMMA")
    ax[2, 0].set_ylabel("arcmin BETA")
    ax[2, 0].plot(
        ___gamma,
        ___beta,
        color="red",
        marker=".",
        markersize=__ms,
        linewidth=0,
    )
    ax[2, 0].axis("equal")
    ax[2, 0].set_xlim(left=-60, right=60)
    ax[2, 0].set_ylim(-50, 50)
    # ax[2, 0].set_xlim(-73.3, 73.3)

    # plot 4Q Sensor graph
    circle2 = plt.Circle((0, 0), 45, color="blue", fill=False)
    ax[2, 1].xaxis.set_major_locator(MultipleLocator(50))
    ax[2, 1].xaxis.set_major_formatter("{x:.0f}")
    ax[2, 1].add_patch(circle2)
    ax[2, 1].set_title("4Q Sensor Eval")
    ax[2, 1].set_xlabel("arcmin GAMMA")
    ax[2, 1].set_ylabel("arcmin BETA")
    ax[2, 1].plot(
        ___gamma,
        ___beta,
        color="red",
        marker=".",
        markersize=__ms,
        linewidth=0,
    )
    ax[2, 1].axis("equal")
    ax[2, 1].set_xlim(left=-120, right=120)
    ax[2, 1].set_ylim(-110, 110)
    # ax[2, 1].set_xlim(-146.67, 146.67)


def plot_SCI_1(hkdata: pd.DataFrame, ax: plt.Axes, mode: str):
    __ms = 0.5

    if mode == "day" or mode == "daily":
        for a in ax.flat:
            a.set_xlabel("Time UTC")
            a.xaxis.set_major_locator(
                mdates.HourLocator(interval=4)
            )  # Set major ticks every 4 hours
            a.xaxis.set_major_formatter(mdates.DateFormatter("%Hh"))
            start_time = mdates.date2num(hkdata["timestamp"].min())
            # end_time = mdates.date2num(hkdata["timestamp"].max())
            end_time = start_time + 1
            a.set_xlim(start_time, end_time)

    if mode == "month" or mode == "monthly":
        for a in ax.flat:
            a.set_xlabel("Date UTC")
            # a.xaxis.set_major_locator(
            #     mdates.DayLocator(bymonthday=range(1, 32, 3), interval=3)
            # )  # Set major ticks every 3 Days
            a.set_xticks(
                mdates.drange(
                    hkdata["timestamp"].min().date(),
                    hkdata["timestamp"].max().date() + datetime.timedelta(1),
                    datetime.timedelta(3),
                )
            )
            a.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y"))

            start_time = mdates.date2num(hkdata["timestamp"].min().date())
            end_time = mdates.date2num(hkdata["timestamp"].max().date())
            a.set_xlim(left=start_time, right=end_time + 1)

    if mode == "year" or mode == "anual":
        for a in ax.flat:
            a.set_xlabel("Date UTC")
            a.xaxis.set_major_locator(
                mdates.MonthLocator()
            )  # Set major ticks every 3 Days
            a.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y"))
            start_time = mdates.date2num(hkdata["timestamp"].min().date())
            end_time = mdates.date2num(hkdata["timestamp"].max().date())
            a.set_xlim(left=start_time, right=end_time + 1)

    if mode == "lifetime":
        for a in ax.flat:
            a.set_xlabel("Date UTC")
            a.xaxis.set_major_locator(
                mdates.MonthLocator(interval=3)
            )  # Set major ticks every 3 Days
            a.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y"))
            start_time = mdates.date2num(hkdata["timestamp"].min())
            end_time = mdates.date2num(hkdata["timestamp"].max())
    if mode == "custom":
        for a in ax.flat:
            a.set_xlabel("Date UTC")
            a.xaxis.set_major_locator(plt.MaxNLocator(12))
            a.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y"))

    for a in ax.flat:
        a.grid(True)
        a.tick_params(axis="x", rotation=30)
        # labels = a.get_xticklabels()
        # for label in labels:
        # label.update({'horizontalalignment': 'right'})

    ax[0, 0].set_title("Calibration Voltages Heater Voltage")
    ax[0, 0].set_ylabel("Heater Voltage [V]")
    ax[0, 0].plot(
        hkdata["timestamp"],
        hkdata["voltage_a"],
        "o",
        color="blue",
        markersize=__ms,
        label="heaterVoltageA",
    )
    ax[0, 0].plot(
        hkdata["timestamp"],
        hkdata["voltage_b"],
        "o",
        color="red",
        markersize=__ms,
        label="heaterVoltageB",
    )
    ax[0, 0].plot(
        hkdata["timestamp"],
        hkdata["voltage_c"],
        "o",
        color="green",
        markersize=__ms,
        label="heaterVoltageC",
    )
    ax[0, 0].set_ylim(0, 5)

    ax[0, 0].legend(
        numpoints=5,
        ncol=2,
        loc="upper right",
    )

    ax[0, 1].set_title("Calibration Voltages Heater Current")
    ax[0, 1].set_ylabel("Shunt Voltage [V]")
    ax[0, 1].plot_date(
        hkdata["timestamp"],
        hkdata["shuntvoltagea"],
        color="blue",
        markersize=__ms,
        label="shuntVoltageA",
    )
    ax[0, 1].plot_date(
        hkdata["timestamp"],
        hkdata["shuntvoltageb"],
        color="red",
        markersize=__ms,
        label="shuntVoltageB",
    )
    ax[0, 1].plot_date(
        hkdata["timestamp"],
        hkdata["shuntvoltagec"],
        color="green",
        markersize=__ms,
        label="shuntVoltageC",
    )
    ax[0, 1].set_ylim(0, 5)
    ax[0, 1].legend(
        numpoints=5,
        ncol=2,
        loc="upper right",
    )

    ax[1, 0].set_title("DAC Voltages")
    if mode == "day" or mode == "daily":
        ax[1, 0].set_xlabel("Time UTC")
    else:
        ax[1, 0].set_xlabel("Date UTC")
    ax[1, 0].set_ylabel("DAC Voltage [V]")
    ax[1, 0].plot_date(
        hkdata["timestamp"],
        hkdata["daca"],
        color="blue",
        markersize=__ms,
        label="dacA",
    )
    ax[1, 0].plot_date(
        hkdata["timestamp"],
        hkdata["dacb"],
        color="red",
        markersize=__ms,
        label="dacB",
    )
    ax[1, 0].plot_date(
        hkdata["timestamp"],
        hkdata["dacc"],
        color="green",
        markersize=__ms,
        label="dacC",
    )
    ax[1, 0].set_ylim(0, 2.5)
    ax[1, 0].legend(numpoints=5, ncol=2, loc="upper right")

    ax[1, 1].set_title("Cavity Assignment")
    ax[1, 1].set_ylabel("CAVITY")
    ax[1, 1].plot_date(
        hkdata["timestamp"],
        hkdata["nominal_cavity"],
        color="blue",
        markersize=__ms,
        linestyle="-",
        linewidth=0.1,
        label="nominal cavity",
    )
    ax[1, 1].plot_date(
        hkdata["timestamp"],
        hkdata["reference_cavity"],
        color="red",
        markersize=__ms,
        linestyle="-",
        linewidth=0.1,
        label="reference cavity",
    )
    ax[1, 1].plot_date(
        hkdata["timestamp"],
        hkdata["backup_cavity_1"],
        color="green",
        markersize=__ms,
        linestyle="-",
        linewidth=0.1,
        label="backup cavity",
    )
    ax[1, 1].set_ylim(-0.15, 3.15)
    ax[1, 1].yaxis.set_major_locator(ticker.FixedLocator([0, 1, 2, 3]))
    ax[1, 1].yaxis.set_major_formatter(
        ticker.FixedFormatter(["none", "A", "B", "C"])
    )
    # ax[1, 1].grid(b="on")
    ax[1, 1].legend(
        numpoints=5,
        ncol=2,
        loc="lower left",
    )

    ax[2, 0].set_title("Shutter 2 Phase Status")
    ax[2, 0].set_ylabel("Shutter")
    ax[2, 0].plot_date(
        hkdata["timestamp"],
        hkdata["shutter_a_2st_phase_open"] + 0,
        color="blue",
        markersize=__ms,
        linestyle="-",
        linewidth=0.1,
        label="Shutter A",
    )
    ax[2, 0].plot_date(
        hkdata["timestamp"],
        hkdata["shutter_b_2st_phase_open"] + 2,
        color="red",
        markersize=__ms,
        linestyle="-",
        linewidth=0.1,
        label="Shutter B",
    )
    ax[2, 0].plot_date(
        hkdata["timestamp"],
        hkdata["shutter_c_2st_phase_open"] + 4,
        color="green",
        markersize=__ms,
        linestyle="-",
        linewidth=0.1,
        label="Shutter C",
    )

    ax[2, 0].set_ylim(-0.15, 5.15)
    ax[2, 0].yaxis.set_major_locator(ticker.FixedLocator([0, 1, 2, 3, 4, 5]))
    ax[2, 0].yaxis.set_major_formatter(
        ticker.FixedFormatter(["A_cl", "A_op", "B_cl", "B_op", "C_cl", "C_op"])
    )
    ax[2, 0].legend(numpoints=5, ncol=2, loc="upper right")

    ax[2, 1].set_title("Shutter 1 Phase Status")
    if mode == "day" or mode == "daily":
        ax[2, 1].set_xlabel("Time UTC")
    else:
        ax[2, 1].set_xlabel("Date UTC")
    ax[2, 1].set_ylabel("Shutter")
    ax[2, 1].plot_date(
        hkdata["timestamp"],
        hkdata["shutter_a_1st_phase_open"] + 0,
        color="blue",
        markersize=__ms,
        linestyle="-",
        linewidth=0.1,
        label="Shutter A",
    )
    ax[2, 1].plot_date(
        hkdata["timestamp"],
        hkdata["shutter_b_1st_phase_open"] + 2,
        color="red",
        markersize=__ms,
        linestyle="-",
        linewidth=0.1,
        label="Shutter B",
    )
    ax[2, 1].plot_date(
        hkdata["timestamp"],
        hkdata["shutter_c_1st_phase_open"] + 4,
        color="green",
        markersize=__ms,
        linestyle="-",
        linewidth=0.1,
        label="Shutter C",
    )

    ax[2, 1].set_ylim(-0.15, 5.15)
    ax[2, 1].yaxis.set_major_locator(ticker.FixedLocator([0, 1, 2, 3, 4, 5]))
    ax[2, 1].yaxis.set_major_formatter(
        ticker.FixedFormatter(["A_cl", "A_op", "B_cl", "B_op", "C_cl", "C_op"])
    )
    # ax[2,1].grid(b='on')
    ax[2, 1].legend(numpoints=5, ncol=2, loc="upper right")


def plot_irr(irr_data: pd.DataFrame, ax: plt.Axes, mode: str = "lifetime"):
    __ms = 0.5
    if mode == "day" or mode == "daily":
        for a in ax.flat:
            a.set_xlabel("Time UTC")
            a.xaxis.set_major_locator(
                mdates.HourLocator(interval=4)
            )  # Set major ticks every 4 hours
            a.xaxis.set_major_formatter(mdates.DateFormatter("%Hh"))
            start_time = mdates.date2num(irr_data["timestamp"].min())
            end_time = start_time + 1
            a.set_xlim(start_time, end_time)

    if mode == "month" or mode == "monthly":
        for a in ax.flat:
            a.set_xlabel("Date UTC")
            # a.xaxis.set_major_locator(
            #     mdates.DayLocator(bymonthday=range(1, 32, 3), interval=3)
            # )  # Set major ticks every 3 Days
            a.set_xticks(
                mdates.drange(
                    irr_data["timestamp"].min().date(),
                    irr_data["timestamp"].max().date() + datetime.timedelta(1),
                    datetime.timedelta(3),
                )
            )
            a.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y"))
            start_time = mdates.date2num(irr_data["timestamp"].min().date())
            end_time = mdates.date2num(irr_data["timestamp"].max().date())
            a.set_xlim(left=start_time, right=end_time + 1)

    if mode == "year" or mode == "anual":
        for a in ax.flat:
            a.set_xlabel("Date UTC")
            a.xaxis.set_major_locator(
                mdates.MonthLocator()
            )  # Set major ticks every month
            a.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y"))

    if mode == "lifetime":
        for a in ax.flat:
            a.set_xlabel("Date UTC")
            a.xaxis.set_major_locator(
                mdates.MonthLocator(interval=3)
            )  # Set major ticks every 3 months
            a.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y"))

    if mode == "custom":
        for a in ax.flat:
            a.set_xlabel("Date UTC")
            a.xaxis.set_major_locator(plt.MaxNLocator(12))
            a.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y"))

    for a in ax.flat:
        a.grid(True)
        a.tick_params(axis="x", rotation=30)
        # labels = a.get_xticklabels()
        # for label in labels:
        # label.update({'horizontalalignment': 'right'})
        a.set_ylim(1355, 1366)

    ax[0].set_title("Irradiance A")
    ax[0].set_ylabel(r"Irradiance [W/m$^2$]")
    ax[0].plot(
        irr_data["timestamp"],
        irr_data["irradiance_a_wm2"],
        "o",
        color="red",
        markersize=__ms,
    )
    ax[1].set_title("Irradiance B")
    ax[1].set_ylabel(r"Irradiance [W/m$^2$]")
    ax[1].plot(
        irr_data["timestamp"],
        irr_data["irradiance_b_wm2"],
        "o",
        color="blue",
        markersize=__ms,
    )
    ax[2].set_title("Irradiance C")
    ax[2].set_ylabel(r"Irradiance [W/m$^2$]")
    ax[2].plot(
        irr_data["timestamp"],
        irr_data["irradiance_c_wm2"],
        "o",
        color="green",
        markersize=__ms,
    )


def plot_parameter(
    param_data: pd.DataFrame, ax: plt.Axes, mode: str = "lifetime"
):
    __ms = 0.5

    if mode == "day" or mode == "daily":
        for a in ax.flat:
            a.set_xlabel("Time UTC")
            a.xaxis.set_major_locator(
                mdates.HourLocator(interval=4)
            )  # Set major ticks every 4 hours
            a.xaxis.set_major_formatter(mdates.DateFormatter("%Hh"))
            start_time = mdates.date2num(param_data["timestamp"].min())
            end_time = start_time + 1
            a.set_xlim(start_time, end_time)

    if mode == "month" or mode == "monthly":
        for a in ax.flat:
            a.set_xlabel("Date UTC")
            # a.xaxis.set_major_locator(
            #     mdates.DayLocator(bymonthday=range(1, 32, 3), interval=3)
            #     # mdates.DayLocator(interval=3)
            # )  # Set major ticks every 3 Days
            a.set_xticks(
                mdates.drange(
                    param_data["timestamp"].min().date(),
                    param_data["timestamp"].max().date()
                    + datetime.timedelta(1),
                    datetime.timedelta(3),
                )
            )
            a.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y"))
            start_time = mdates.date2num(param_data["timestamp"].min().date())
            end_time = mdates.date2num(param_data["timestamp"].max().date())
            a.set_xlim(left=start_time, right=end_time + 1)

    if mode == "year" or mode == "anual":
        for a in ax.flat:
            a.set_xlabel("Date UTC")
            a.xaxis.set_major_locator(
                mdates.MonthLocator()
            )  # Set major ticks every month
            a.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y"))

    if mode == "lifetime":
        for a in ax.flat:
            a.set_xlabel("Date UTC")
            a.xaxis.set_major_locator(
                mdates.MonthLocator(interval=3)
            )  # Set major ticks every 3 months
            a.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y"))

    if mode == "custom":
        for a in ax.flat:
            a.set_xlabel("Date UTC")
            a.xaxis.set_major_locator(plt.MaxNLocator(12))
            a.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y"))

    for a in ax.flat:
        a.grid(True)
        a.tick_params(axis="x", rotation=30)
        # labels = a.get_xticklabels()
        # for label in labels:
        # label.update({'horizontalalignment': 'right'})

    ax[0, 0].set_title("Parameter ttu/thk")
    ax[0, 0].set_ylabel("Interval Time [s]")
    ax[0, 0].plot(
        param_data["timestamp"],
        param_data["ttu"],
        "o",
        color="blue",
        markersize=__ms,
    )
    ax[0, 0].plot(
        param_data["timestamp"],
        param_data["thk"],
        "o",
        color="red",
        markersize=__ms,
    )
    y_min, y_max = ax[0, 0].get_ylim()
    ax[0, 0].set_ylim(y_min, y_max * 1.25)
    ax[0, 0].legend(["ttu", "thk"], numpoints=5, ncol=2, loc="upper right")

    ax[0, 1].set_title("Parameter iss/ima/imb/imc")
    ax[0, 1].set_ylabel("Value [number]")
    ax[0, 1].plot(
        param_data["timestamp"],
        param_data["iss"],
        "o",
        color="blue",
        markersize=__ms,
        label="iss",
    )
    ax[0, 1].plot(
        param_data["timestamp"],
        param_data["ima"],
        "o",
        color="red",
        markersize=__ms,
        label="ima",
    )
    ax[0, 1].plot(
        param_data["timestamp"],
        param_data["imb"],
        "o",
        color="green",
        markersize=__ms,
        label="imb",
    )
    ax[0, 1].plot(
        param_data["timestamp"],
        param_data["imc"],
        "o",
        color="cyan",
        markersize=__ms,
        label="imc",
    )
    y_min, y_max = ax[0, 1].get_ylim()
    ax[0, 1].set_ylim(min(y_min, 0), y_max * 1.25)
    ax[0, 1].legend(numpoints=5, ncol=2, loc="upper right")

    ax[1, 0].set_title("Parameter ucr")
    ax[1, 0].set_ylabel("Voltage [V]")
    ax[1, 0].plot(
        param_data["timestamp"],
        param_data["ucr"],
        "o",
        color="blue",
        markersize=__ms,
    )
    y_min, y_max = ax[1, 0].get_ylim()
    ax[1, 0].set_ylim(min(y_min, 0), y_max * 1.25)
    ax[1, 0].legend(["ucr"], numpoints=5, ncol=2, loc="upper right")

    ax[1, 1].set_title("Parameter apo/aio/ado/apc/aic/adc")
    ax[1, 1].set_ylabel("Value")
    ax[1, 1].plot(
        param_data["timestamp"],
        param_data["apo"],
        "o",
        color="blue",
        markersize=__ms,
        label="apo",
    )
    ax[1, 1].plot(
        param_data["timestamp"],
        param_data["aio"],
        "o",
        color="red",
        markersize=__ms,
        label="aio",
    )
    ax[1, 1].plot(
        param_data["timestamp"],
        param_data["ado"],
        "o",
        color="green",
        markersize=__ms,
        label="ado",
    )
    ax[1, 1].plot(
        param_data["timestamp"],
        param_data["apc"],
        "o",
        color="cyan",
        markersize=__ms,
        label="apc",
    )
    ax[1, 1].plot(
        param_data["timestamp"],
        param_data["aic"],
        "o",
        color="magenta",
        markersize=__ms,
        label="aic",
    )
    ax[1, 1].plot(
        param_data["timestamp"],
        param_data["adc"],
        "o",
        color="yellow",
        markersize=__ms,
        label="adc",
    )
    y_min, y_max = ax[1, 1].get_ylim()
    ax[1, 1].set_ylim(min(y_min, 0), 0.1)
    ax[1, 1].legend(numpoints=5, ncol=2, loc="upper right")

    ax[2, 0].set_title("Parameter bpo/bio/bdo/bpc/bic/bdc")
    ax[2, 0].set_ylabel("Value")
    ax[2, 0].plot(
        param_data["timestamp"],
        param_data["bpo"],
        "o",
        color="blue",
        markersize=__ms,
        label="bpo",
    )
    ax[2, 0].plot(
        param_data["timestamp"],
        param_data["bio"],
        "o",
        color="red",
        markersize=__ms,
        label="bio",
    )
    ax[2, 0].plot(
        param_data["timestamp"],
        param_data["bdo"],
        "o",
        color="green",
        markersize=__ms,
        label="bdo",
    )
    ax[2, 0].plot(
        param_data["timestamp"],
        param_data["bpc"],
        "o",
        color="cyan",
        markersize=__ms,
        label="bpc",
    )
    ax[2, 0].plot(
        param_data["timestamp"],
        param_data["bic"],
        "o",
        color="magenta",
        markersize=__ms,
        label="bic",
    )
    ax[2, 0].plot(
        param_data["timestamp"],
        param_data["bdc"],
        "o",
        color="yellow",
        markersize=__ms,
        label="bdc",
    )
    y_min, y_max = ax[2, 0].get_ylim()
    ax[2, 0].set_ylim(min(y_min, 0), 0.1)
    ax[2, 0].legend(numpoints=5, ncol=2, loc="upper right")

    ax[2, 1].set_title("Parameter cpo/cio/cdo/cpc/cic/cdc")
    ax[2, 1].set_ylabel("Value")
    ax[2, 1].plot(
        param_data["timestamp"],
        param_data["cpo"],
        "o",
        color="blue",
        markersize=__ms,
        label="cpo",
    )
    ax[2, 1].plot(
        param_data["timestamp"],
        param_data["cio"],
        "o",
        color="red",
        markersize=__ms,
        label="cio",
    )
    ax[2, 1].plot(
        param_data["timestamp"],
        param_data["cdo"],
        "o",
        color="green",
        markersize=__ms,
        label="cdo",
    )
    ax[2, 1].plot(
        param_data["timestamp"],
        param_data["cpc"],
        "o",
        color="cyan",
        markersize=__ms,
        label="cpc",
    )
    ax[2, 1].plot(
        param_data["timestamp"],
        param_data["cic"],
        "o",
        color="magenta",
        markersize=__ms,
        label="cic",
    )
    ax[2, 1].plot(
        param_data["timestamp"],
        param_data["cdc"],
        "o",
        color="yellow",
        markersize=__ms,
        label="cdc",
    )
    y_min, y_max = ax[2, 1].get_ylim()
    ax[2, 1].set_ylim(min(y_min, 0), 0.1)
    ax[2, 1].legend(numpoints=5, ncol=2, loc="upper right")
