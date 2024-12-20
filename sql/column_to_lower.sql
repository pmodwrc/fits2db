ALTER TABLE calibration RENAME COLUMN `BACKUP_CAVITY` TO `backup_cavity`;
ALTER TABLE calibration RENAME COLUMN `BACKUP_CAVITY_1` TO `backup_cavity_1`;
ALTER TABLE calibration RENAME COLUMN `CNTR` TO `cntr`;
ALTER TABLE calibration RENAME COLUMN `CURRENT_A` TO `current_a`;
ALTER TABLE calibration RENAME COLUMN `CURRENT_B` TO `current_b`;
ALTER TABLE calibration RENAME COLUMN `CURRENT_C` TO `current_c`;
ALTER TABLE calibration RENAME COLUMN `CYCLE_INDEX` TO `cycle_index`;
ALTER TABLE calibration RENAME COLUMN `DACA` TO `daca`;
ALTER TABLE calibration RENAME COLUMN `DACB` TO `dacb`;
ALTER TABLE calibration RENAME COLUMN `DACC` TO `dacc`;
ALTER TABLE calibration RENAME COLUMN `FILE_META_ID` TO `file_meta_id`;
ALTER TABLE calibration RENAME COLUMN `HEAT_SINK_HEATER_USED` TO `heat_sink_heater_used`;
ALTER TABLE calibration RENAME COLUMN `HEATERVOLTAGEA` TO `heatervoltagea`;
ALTER TABLE calibration RENAME COLUMN `HEATERVOLTAGEB` TO `heatervoltageb`;
ALTER TABLE calibration RENAME COLUMN `HEATERVOLTAGEC` TO `heatervoltagec`;
ALTER TABLE calibration RENAME COLUMN `id` TO `id`;
ALTER TABLE calibration RENAME COLUMN `MODE` TO `mode`;
ALTER TABLE calibration RENAME COLUMN `NOMINAL_CAVITY` TO `nominal_cavity`;
ALTER TABLE calibration RENAME COLUMN `REFERENCE_CAVITY` TO `reference_cavity`;
ALTER TABLE calibration RENAME COLUMN `SAMPLEINTERVAL` TO `sampleinterval`;
ALTER TABLE calibration RENAME COLUMN `SAMPLEOFFSET` TO `sampleoffset`;
ALTER TABLE calibration RENAME COLUMN `SHUNTVOLTAGEA` TO `shuntvoltagea`;
ALTER TABLE calibration RENAME COLUMN `SHUNTVOLTAGEB` TO `shuntvoltageb`;
ALTER TABLE calibration RENAME COLUMN `SHUNTVOLTAGEC` TO `shuntvoltagec`;
ALTER TABLE calibration RENAME COLUMN `SHUTTER_A_1ST_PHASE_OPEN` TO `shutter_a_1st_phase_open`;
ALTER TABLE calibration RENAME COLUMN `SHUTTER_A_2ST_PHASE_OPEN` TO `shutter_a_2st_phase_open`;
ALTER TABLE calibration RENAME COLUMN `SHUTTER_B_1ST_PHASE_OPEN` TO `shutter_b_1st_phase_open`;
ALTER TABLE calibration RENAME COLUMN `SHUTTER_B_2ST_PHASE_OPEN` TO `shutter_b_2st_phase_open`;
ALTER TABLE calibration RENAME COLUMN `SHUTTER_C_1ST_PHASE_OPEN` TO `shutter_c_1st_phase_open`;
ALTER TABLE calibration RENAME COLUMN `SHUTTER_C_2ST_PHASE_OPEN` TO `shutter_c_2st_phase_open`;
ALTER TABLE calibration RENAME COLUMN `TIME` TO `time`;
ALTER TABLE calibration RENAME COLUMN `timestamp` TO `timestamp`;
ALTER TABLE calibration RENAME COLUMN `VOLTAGE_A` TO `voltage_a`;
ALTER TABLE calibration RENAME COLUMN `VOLTAGE_B` TO `voltage_b`;
ALTER TABLE calibration RENAME COLUMN `VOLTAGE_C` TO `voltage_c`;
ALTER TABLE calibration_meta RENAME COLUMN `KEYWORD` TO `keyword`;
ALTER TABLE calibration_meta RENAME COLUMN `VALUE` TO `value`;
ALTER TABLE cavity_exposure RENAME COLUMN `CNTR` TO `cntr`;
ALTER TABLE cavity_exposure RENAME COLUMN `CSECSA` TO `csecsa`;
ALTER TABLE cavity_exposure RENAME COLUMN `CSECSB` TO `csecsb`;
ALTER TABLE cavity_exposure RENAME COLUMN `CSECSC` TO `csecsc`;
ALTER TABLE cavity_exposure RENAME COLUMN `CYCLE_INDEX` TO `cycle_index`;
ALTER TABLE cavity_exposure RENAME COLUMN `FILE_META_ID` TO `file_meta_id`;
ALTER TABLE cavity_exposure RENAME COLUMN `id` TO `id`;
ALTER TABLE cavity_exposure RENAME COLUMN `MODE` TO `mode`;
ALTER TABLE cavity_exposure RENAME COLUMN `SAMPLEINTERVAL` TO `sampleinterval`;
ALTER TABLE cavity_exposure RENAME COLUMN `SAMPLEOFFSET` TO `sampleoffset`;
ALTER TABLE cavity_exposure RENAME COLUMN `SECSA` TO `secsa`;
ALTER TABLE cavity_exposure RENAME COLUMN `SECSB` TO `secsb`;
ALTER TABLE cavity_exposure RENAME COLUMN `SECSC` TO `secsc`;
ALTER TABLE cavity_exposure RENAME COLUMN `TIME` TO `time`;
ALTER TABLE cavity_exposure RENAME COLUMN `TIMESTAMP` TO `timestamp`;
ALTER TABLE cavity_exposure_meta RENAME COLUMN `KEYWORD` TO `keyword`;
ALTER TABLE cavity_exposure_meta RENAME COLUMN `VALUE` TO `value`;
ALTER TABLE fits2db_meta RENAME COLUMN `filename` TO `filename`;
ALTER TABLE fits2db_meta RENAME COLUMN `filepath` TO `filepath`;
ALTER TABLE fits2db_meta RENAME COLUMN `id` TO `id`;
ALTER TABLE fits2db_meta RENAME COLUMN `last_db_update` TO `last_db_update`;
ALTER TABLE fits2db_meta RENAME COLUMN `last_file_mutation` TO `last_file_mutation`;
ALTER TABLE fits2db_table_meta RENAME COLUMN `column_count` TO `column_count`;
ALTER TABLE fits2db_table_meta RENAME COLUMN `file_meta_id` TO `file_meta_id`;
ALTER TABLE fits2db_table_meta RENAME COLUMN `id` TO `id`;
ALTER TABLE fits2db_table_meta RENAME COLUMN `record_count` TO `record_count`;
ALTER TABLE fits2db_table_meta RENAME COLUMN `tablename` TO `tablename`;
ALTER TABLE housekeeping RENAME COLUMN `ADC128S_2V5` TO `adc128s_2v5`;
ALTER TABLE housekeeping RENAME COLUMN `ADC128S_5V` TO `adc128s_5v`;
ALTER TABLE housekeeping RENAME COLUMN `ADC128S_AGND` TO `adc128s_agnd`;
ALTER TABLE housekeeping RENAME COLUMN `ADC128S_CURR_SENSE` TO `adc128s_curr_sense`;
ALTER TABLE housekeeping RENAME COLUMN `BETA` TO `beta`;
ALTER TABLE housekeeping RENAME COLUMN `CAV_HEATSINK_TEMP` TO `cav_heatsink_temp`;
ALTER TABLE housekeeping RENAME COLUMN `CAV_HS_HEATER_VOLTAGE` TO `cav_hs_heater_voltage`;
ALTER TABLE housekeeping RENAME COLUMN `CAV_INST_A_U_TEMP` TO `cav_inst_a_u_temp`;
ALTER TABLE housekeeping RENAME COLUMN `CAV_INST_B_U_TEMP` TO `cav_inst_b_u_temp`;
ALTER TABLE housekeeping RENAME COLUMN `CAV_INST_C_U_TEMP` TO `cav_inst_c_u_temp`;
ALTER TABLE housekeeping RENAME COLUMN `CNTR` TO `cntr`;
ALTER TABLE housekeeping RENAME COLUMN `CPU_ADC_TEMP` TO `cpu_adc_temp`;
ALTER TABLE housekeeping RENAME COLUMN `CPU_AGND0` TO `cpu_agnd0`;
ALTER TABLE housekeeping RENAME COLUMN `CPU_AGND1` TO `cpu_agnd1`;
ALTER TABLE housekeeping RENAME COLUMN `CPU_AGND2` TO `cpu_agnd2`;
ALTER TABLE housekeeping RENAME COLUMN `CPU_AGND3` TO `cpu_agnd3`;
ALTER TABLE housekeeping RENAME COLUMN `CPU_AGND4` TO `cpu_agnd4`;
ALTER TABLE housekeeping RENAME COLUMN `CPU_AGND5` TO `cpu_agnd5`;
ALTER TABLE housekeeping RENAME COLUMN `CPU_AGND6` TO `cpu_agnd6`;
ALTER TABLE housekeeping RENAME COLUMN `CPU_AGND7` TO `cpu_agnd7`;
ALTER TABLE housekeeping RENAME COLUMN `CPU_CPU_TEMP` TO `cpu_cpu_temp`;
ALTER TABLE housekeeping RENAME COLUMN `CPU_HKREF_TEMP` TO `cpu_hkref_temp`;
ALTER TABLE housekeeping RENAME COLUMN `CPU_MRAM_TEMP` TO `cpu_mram_temp`;
ALTER TABLE housekeeping RENAME COLUMN `CPU_OSC_TEMP` TO `cpu_osc_temp`;
ALTER TABLE housekeeping RENAME COLUMN `CPU_SRAM_TEMP` TO `cpu_sram_temp`;
ALTER TABLE housekeeping RENAME COLUMN `CPU_VCC` TO `cpu_vcc`;
ALTER TABLE housekeeping RENAME COLUMN `CPU_VCC_3V3` TO `cpu_vcc_3v3`;
ALTER TABLE housekeeping RENAME COLUMN `DAQ_A_TEMP` TO `daq_a_temp`;
ALTER TABLE housekeeping RENAME COLUMN `DAQ_B_TEMP` TO `daq_b_temp`;
ALTER TABLE housekeeping RENAME COLUMN `DAQ_C_TEMP` TO `daq_c_temp`;
ALTER TABLE housekeeping RENAME COLUMN `DAQ_D_TEMP` TO `daq_d_temp`;
ALTER TABLE housekeeping RENAME COLUMN `DAQ_E_TEMP` TO `daq_e_temp`;
ALTER TABLE housekeeping RENAME COLUMN `DAQ_HK_REF_MON` TO `daq_hk_ref_mon`;
ALTER TABLE housekeeping RENAME COLUMN `DAQ_HS_DAC_OUT` TO `daq_hs_dac_out`;
ALTER TABLE housekeeping RENAME COLUMN `DAQ_INST_A_I_TEMP` TO `daq_inst_a_i_temp`;
ALTER TABLE housekeeping RENAME COLUMN `DAQ_INST_B_I_TEMP` TO `daq_inst_b_i_temp`;
ALTER TABLE housekeeping RENAME COLUMN `DAQ_INST_C_I_TEMP` TO `daq_inst_c_i_temp`;
ALTER TABLE housekeeping RENAME COLUMN `DAQ_REF_TEMP` TO `daq_ref_temp`;
ALTER TABLE housekeeping RENAME COLUMN `DAY` TO `day`;
ALTER TABLE housekeeping RENAME COLUMN `DCDC_12VDCDC_TEMP` TO `dcdc_12vdcdc_temp`;
ALTER TABLE housekeeping RENAME COLUMN `DCDC_12VNEG_CM` TO `dcdc_12vneg_cm`;
ALTER TABLE housekeeping RENAME COLUMN `DCDC_12VNEG_PROT` TO `dcdc_12vneg_prot`;
ALTER TABLE housekeeping RENAME COLUMN `DCDC_12VPOS_CM` TO `dcdc_12vpos_cm`;
ALTER TABLE housekeeping RENAME COLUMN `DCDC_12VPOS_PROT` TO `dcdc_12vpos_prot`;
ALTER TABLE housekeeping RENAME COLUMN `DCDC_28V_PRIM_CURRENT` TO `dcdc_28v_prim_current`;
ALTER TABLE housekeeping RENAME COLUMN `DCDC_5VDCDC_TEMP` TO `dcdc_5vdcdc_temp`;
ALTER TABLE housekeeping RENAME COLUMN `DCDC_5VPOS_A_CM` TO `dcdc_5vpos_a_cm`;
ALTER TABLE housekeeping RENAME COLUMN `DCDC_5VPOS_A_PROT` TO `dcdc_5vpos_a_prot`;
ALTER TABLE housekeeping RENAME COLUMN `DCDC_5VPOS_D_CM` TO `dcdc_5vpos_d_cm`;
ALTER TABLE housekeeping RENAME COLUMN `DCDC_5VPOS_D_PROT` TO `dcdc_5vpos_d_prot`;
ALTER TABLE housekeeping RENAME COLUMN `DCDC_AGND0` TO `dcdc_agnd0`;
ALTER TABLE housekeeping RENAME COLUMN `DCDC_CS_TEMP` TO `dcdc_cs_temp`;
ALTER TABLE housekeeping RENAME COLUMN `DCDC_DGND0` TO `dcdc_dgnd0`;
ALTER TABLE housekeeping RENAME COLUMN `DCDC_DGND1` TO `dcdc_dgnd1`;
ALTER TABLE housekeeping RENAME COLUMN `DCDC_ICL_TEMP` TO `dcdc_icl_temp`;
ALTER TABLE housekeeping RENAME COLUMN `FILE_META_ID` TO `file_meta_id`;
ALTER TABLE housekeeping RENAME COLUMN `GAMMA` TO `gamma`;
ALTER TABLE housekeeping RENAME COLUMN `id` TO `id`;
ALTER TABLE housekeeping RENAME COLUMN `MODE` TO `mode`;
ALTER TABLE housekeeping RENAME COLUMN `MONTH` TO `month`;
ALTER TABLE housekeeping RENAME COLUMN `SAMPLEINTERVAL` TO `sampleinterval`;
ALTER TABLE housekeeping RENAME COLUMN `SAMPLEOFFSET` TO `sampleoffset`;
ALTER TABLE housekeeping RENAME COLUMN `SB_4QA` TO `sb_4qa`;
ALTER TABLE housekeeping RENAME COLUMN `SB_4QB` TO `sb_4qb`;
ALTER TABLE housekeeping RENAME COLUMN `SB_4QC` TO `sb_4qc`;
ALTER TABLE housekeeping RENAME COLUMN `SB_4QD` TO `sb_4qd`;
ALTER TABLE housekeeping RENAME COLUMN `SB_BOTTOM_TEMP` TO `sb_bottom_temp`;
ALTER TABLE housekeeping RENAME COLUMN `SB_CASE_TEMP` TO `sb_case_temp`;
ALTER TABLE housekeeping RENAME COLUMN `SB_MCU_TEMP` TO `sb_mcu_temp`;
ALTER TABLE housekeeping RENAME COLUMN `SB_MOT_A_TEMP` TO `sb_mot_a_temp`;
ALTER TABLE housekeeping RENAME COLUMN `SB_MOT_B_TEMP` TO `sb_mot_b_temp`;
ALTER TABLE housekeeping RENAME COLUMN `SB_MOT_C_TEMP` TO `sb_mot_c_temp`;
ALTER TABLE housekeeping RENAME COLUMN `SB_REG_A_TEMP` TO `sb_reg_a_temp`;
ALTER TABLE housekeeping RENAME COLUMN `SB_REG_B_TEMP` TO `sb_reg_b_temp`;
ALTER TABLE housekeeping RENAME COLUMN `SB_REG_C_TEMP` TO `sb_reg_c_temp`;
ALTER TABLE housekeeping RENAME COLUMN `SB_SHA_BOARD_TEMP` TO `sb_sha_board_temp`;
ALTER TABLE housekeeping RENAME COLUMN `SB_SHB_BOARD_TEMP` TO `sb_shb_board_temp`;
ALTER TABLE housekeeping RENAME COLUMN `SB_SHC_BOARD_TEMP` TO `sb_shc_board_temp`;
ALTER TABLE housekeeping RENAME COLUMN `TIME` TO `time`;
-- ALTER TABLE housekeeping RENAME COLUMN `timestamp` TO `timestamp`;
ALTER TABLE housekeeping RENAME COLUMN `YEAR` TO `year`;
ALTER TABLE housekeeping_meta RENAME COLUMN `KEYWORD` TO `keyword`;
ALTER TABLE housekeeping_meta RENAME COLUMN `VALUE` TO `value`;
ALTER TABLE jtsim_broadcast RENAME COLUMN `ATTITUDE_PHI` TO `attitude_phi`;
ALTER TABLE jtsim_broadcast RENAME COLUMN `ATTITUDE_PSI` TO `attitude_psi`;
ALTER TABLE jtsim_broadcast RENAME COLUMN `ATTITUDE_THETA` TO `attitude_theta`;
ALTER TABLE jtsim_broadcast RENAME COLUMN `ATTITUDE_TIME` TO `attitude_time`;
ALTER TABLE jtsim_broadcast RENAME COLUMN `CNTR` TO `cntr`;
ALTER TABLE jtsim_broadcast RENAME COLUMN `FILE_META_ID` TO `file_meta_id`;
ALTER TABLE jtsim_broadcast RENAME COLUMN `GPS_TIME` TO `gps_time`;
ALTER TABLE jtsim_broadcast RENAME COLUMN `GPS_X` TO `gps_x`;
ALTER TABLE jtsim_broadcast RENAME COLUMN `GPS_Y` TO `gps_y`;
ALTER TABLE jtsim_broadcast RENAME COLUMN `GPS_Z` TO `gps_z`;
ALTER TABLE jtsim_broadcast RENAME COLUMN `id` TO `id`;
ALTER TABLE jtsim_broadcast RENAME COLUMN `MODE` TO `mode`;
ALTER TABLE jtsim_broadcast RENAME COLUMN `SAMPLEINTERVAL` TO `sampleinterval`;
ALTER TABLE jtsim_broadcast RENAME COLUMN `SAMPLEOFFSET` TO `sampleoffset`;
ALTER TABLE jtsim_broadcast RENAME COLUMN `SUNSENSOR_ROLL` TO `sunsensor_roll`;
ALTER TABLE jtsim_broadcast RENAME COLUMN `SUNSENSOR_ROLLHIGH` TO `sunsensor_rollhigh`;
ALTER TABLE jtsim_broadcast RENAME COLUMN `SUNSENSOR_ROLLLOW` TO `sunsensor_rolllow`;
ALTER TABLE jtsim_broadcast RENAME COLUMN `SUNSENSOR_YAW` TO `sunsensor_yaw`;
ALTER TABLE jtsim_broadcast RENAME COLUMN `SUNSENSOR_YAWHIGH` TO `sunsensor_yawhigh`;
ALTER TABLE jtsim_broadcast RENAME COLUMN `SUNSENSOR_YAWLOW` TO `sunsensor_yawlow`;
ALTER TABLE jtsim_broadcast RENAME COLUMN `SUNVECTOR_X` TO `sunvector_x`;
ALTER TABLE jtsim_broadcast RENAME COLUMN `SUNVECTOR_Y` TO `sunvector_y`;
ALTER TABLE jtsim_broadcast RENAME COLUMN `SUNVECTOR_Z` TO `sunvector_z`;
ALTER TABLE jtsim_broadcast RENAME COLUMN `TEMP_IFSB` TO `temp_ifsb`;
ALTER TABLE jtsim_broadcast RENAME COLUMN `TIME` TO `time`;
ALTER TABLE jtsim_broadcast RENAME COLUMN `TIME_DAYS` TO `time_days`;
ALTER TABLE jtsim_broadcast RENAME COLUMN `TIME_MS` TO `time_ms`;
ALTER TABLE jtsim_broadcast RENAME COLUMN `TIMESTAMP` TO `timestamp`;
ALTER TABLE jtsim_broadcast_meta RENAME COLUMN `KEYWORD` TO `keyword`;
ALTER TABLE jtsim_broadcast_meta RENAME COLUMN `VALUE` TO `value`;
ALTER TABLE parameterset RENAME COLUMN `ADC` TO `adc`;
ALTER TABLE parameterset RENAME COLUMN `ADO` TO `ado`;
ALTER TABLE parameterset RENAME COLUMN `AIC` TO `aic`;
ALTER TABLE parameterset RENAME COLUMN `AIO` TO `aio`;
ALTER TABLE parameterset RENAME COLUMN `APC` TO `apc`;
ALTER TABLE parameterset RENAME COLUMN `APO` TO `apo`;
ALTER TABLE parameterset RENAME COLUMN `BDC` TO `bdc`;
ALTER TABLE parameterset RENAME COLUMN `BDO` TO `bdo`;
ALTER TABLE parameterset RENAME COLUMN `BIC` TO `bic`;
ALTER TABLE parameterset RENAME COLUMN `BIO` TO `bio`;
ALTER TABLE parameterset RENAME COLUMN `BPC` TO `bpc`;
ALTER TABLE parameterset RENAME COLUMN `BPO` TO `bpo`;
ALTER TABLE parameterset RENAME COLUMN `CDC` TO `cdc`;
ALTER TABLE parameterset RENAME COLUMN `CDO` TO `cdo`;
ALTER TABLE parameterset RENAME COLUMN `CIC` TO `cic`;
ALTER TABLE parameterset RENAME COLUMN `CIO` TO `cio`;
ALTER TABLE parameterset RENAME COLUMN `CNTR` TO `cntr`;
ALTER TABLE parameterset RENAME COLUMN `CPC` TO `cpc`;
ALTER TABLE parameterset RENAME COLUMN `CPO` TO `cpo`;
ALTER TABLE parameterset RENAME COLUMN `CYCLE_INDEX` TO `cycle_index`;
ALTER TABLE parameterset RENAME COLUMN `DSE` TO `dse`;
ALTER TABLE parameterset RENAME COLUMN `DSS` TO `dss`;
ALTER TABLE parameterset RENAME COLUMN `FILE_META_ID` TO `file_meta_id`;
ALTER TABLE parameterset RENAME COLUMN `FSY` TO `fsy`;
ALTER TABLE parameterset RENAME COLUMN `HST` TO `hst`;
ALTER TABLE parameterset RENAME COLUMN `id` TO `id`;
ALTER TABLE parameterset RENAME COLUMN `IMA` TO `ima`;
ALTER TABLE parameterset RENAME COLUMN `IMB` TO `imb`;
ALTER TABLE parameterset RENAME COLUMN `IMC` TO `imc`;
ALTER TABLE parameterset RENAME COLUMN `ISS` TO `iss`;
ALTER TABLE parameterset RENAME COLUMN `IVC` TO `ivc`;
ALTER TABLE parameterset RENAME COLUMN `IVO` TO `ivo`;
ALTER TABLE parameterset RENAME COLUMN `LLO` TO `llo`;
ALTER TABLE parameterset RENAME COLUMN `LPT` TO `lpt`;
ALTER TABLE parameterset RENAME COLUMN `LUP` TO `lup`;
ALTER TABLE parameterset RENAME COLUMN `MODE` TO `mode`;
ALTER TABLE parameterset RENAME COLUMN `NSR` TO `nsr`;
ALTER TABLE parameterset RENAME COLUMN `RCH` TO `rch`;
ALTER TABLE parameterset RENAME COLUMN `SAMPLEINTERVAL` TO `sampleinterval`;
ALTER TABLE parameterset RENAME COLUMN `SAMPLEOFFSET` TO `sampleoffset`;
ALTER TABLE parameterset RENAME COLUMN `SSC` TO `ssc`;
ALTER TABLE parameterset RENAME COLUMN `THK` TO `thk`;
ALTER TABLE parameterset RENAME COLUMN `TIME` TO `time`;
ALTER TABLE parameterset RENAME COLUMN `TIMESTAMP` TO `timestamp`;
ALTER TABLE parameterset RENAME COLUMN `TSP` TO `tsp`;
ALTER TABLE parameterset RENAME COLUMN `TTU` TO `ttu`;
ALTER TABLE parameterset RENAME COLUMN `UCC` TO `ucc`;
ALTER TABLE parameterset RENAME COLUMN `UCR` TO `ucr`;
ALTER TABLE parameterset RENAME COLUMN `URE` TO `ure`;
ALTER TABLE parameterset RENAME COLUMN `URH` TO `urh`;
ALTER TABLE parameterset_meta RENAME COLUMN `KEYWORD` TO `keyword`;
ALTER TABLE parameterset_meta RENAME COLUMN `VALUE` TO `value`;
ALTER TABLE shutter RENAME COLUMN `CNTR` TO `cntr`;
ALTER TABLE shutter RENAME COLUMN `CYCLE_INDEX` TO `cycle_index`;
ALTER TABLE shutter RENAME COLUMN `FILE_META_ID` TO `file_meta_id`;
ALTER TABLE shutter RENAME COLUMN `id` TO `id`;
ALTER TABLE shutter RENAME COLUMN `MODE` TO `mode`;
ALTER TABLE shutter RENAME COLUMN `SAMPLEINTERVAL` TO `sampleinterval`;
ALTER TABLE shutter RENAME COLUMN `SAMPLEOFFSET` TO `sampleoffset`;
ALTER TABLE shutter RENAME COLUMN `SHUTTER` TO `shutter`;
ALTER TABLE shutter RENAME COLUMN `SHUTTER_A_OPEN` TO `shutter_a_open`;
ALTER TABLE shutter RENAME COLUMN `SHUTTER_B_OPEN` TO `shutter_b_open`;
ALTER TABLE shutter RENAME COLUMN `SHUTTER_C_OPEN` TO `shutter_c_open`;
ALTER TABLE shutter RENAME COLUMN `TIME` TO `time`;
ALTER TABLE shutter RENAME COLUMN `TIMESTAMP` TO `timestamp`;
ALTER TABLE shutter_meta RENAME COLUMN `KEYWORD` TO `keyword`;
ALTER TABLE shutter_meta RENAME COLUMN `VALUE` TO `value`;
ALTER TABLE telemetry RENAME COLUMN `adcselftest1` TO `adcselftest1`;
ALTER TABLE telemetry RENAME COLUMN `adcselftest2` TO `adcselftest2`;
ALTER TABLE telemetry RENAME COLUMN `adcselftest3` TO `adcselftest3`;
ALTER TABLE telemetry RENAME COLUMN `ccsdsstatusreg` TO `ccsdsstatusreg`;
ALTER TABLE telemetry RENAME COLUMN `cntr` TO `cntr`;
ALTER TABLE telemetry RENAME COLUMN `file_meta_id` TO `file_meta_id`;
ALTER TABLE telemetry RENAME COLUMN `hdxfpoolheadcntr` TO `hdxfpoolheadcntr`;
ALTER TABLE telemetry RENAME COLUMN `heapheadsize` TO `heapheadsize`;
ALTER TABLE telemetry RENAME COLUMN `id` TO `id`;
ALTER TABLE telemetry RENAME COLUMN `idlecountperiod` TO `idlecountperiod`;
ALTER TABLE telemetry RENAME COLUMN `mode` TO `mode`;
ALTER TABLE telemetry RENAME COLUMN `msgpoolheadcntr` TO `msgpoolheadcntr`;
ALTER TABLE telemetry RENAME COLUMN `perifstatusreg` TO `perifstatusreg`;
ALTER TABLE telemetry RENAME COLUMN `radiometerstatusreg` TO `radiometerstatusreg`;
ALTER TABLE telemetry RENAME COLUMN `sampleinterval` TO `sampleinterval`;
ALTER TABLE telemetry RENAME COLUMN `sampleoffset` TO `sampleoffset`;
ALTER TABLE telemetry RENAME COLUMN `serialstatusreg` TO `serialstatusreg`;
ALTER TABLE telemetry RENAME COLUMN `shutterbootstatusreg` TO `shutterbootstatusreg`;
ALTER TABLE telemetry RENAME COLUMN `shutterexpectedstatusreg` TO `shutterexpectedstatusreg`;
ALTER TABLE telemetry RENAME COLUMN `shutterstatusreg` TO `shutterstatusreg`;
ALTER TABLE telemetry RENAME COLUMN `stackmaxusage` TO `stackmaxusage`;
ALTER TABLE telemetry RENAME COLUMN `sysstatusreg` TO `sysstatusreg`;
ALTER TABLE telemetry RENAME COLUMN `taskstatusreg` TO `taskstatusreg`;
ALTER TABLE telemetry RENAME COLUMN `time` TO `time`;
ALTER TABLE telemetry RENAME COLUMN `timestamp` TO `timestamp`;
ALTER TABLE telemetry_meta RENAME COLUMN `KEYWORD` TO `keyword`;
ALTER TABLE telemetry_meta RENAME COLUMN `VALUE` TO `value`;
