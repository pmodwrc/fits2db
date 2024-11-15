ALTER TABLE calibration MODIFY COLUMN `timestamp` datetime;
ALTER TABLE cavity_exposure MODIFY COLUMN `timestamp` datetime;
ALTER TABLE housekeeping MODIFY COLUMN `timestamp` datetime;
ALTER TABLE jtsim_broadcast MODIFY COLUMN `timestamp` datetime;
ALTER TABLE parameterset MODIFY COLUMN `timestamp` datetime;
ALTER TABLE shutter MODIFY COLUMN `timestamp` datetime;
ALTER TABLE telemetry MODIFY COLUMN `timestamp` datetime;
