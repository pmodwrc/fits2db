<p align="center">
    <img src="https://raw.githubusercontent.com/pmodwrc/fits2db/main/docs/layout/images/fits_logo.png" alt="fits2db" width="500"/>
</p>

-----------------

# fits2db: A cli tool to ingest fits files into an sql db
| | |
| --- | --- |
| __Testing__ | [![CI - Test](https://img.shields.io/github/actions/workflow/status/pmodwrc/fits2db/unit_test.yml?branch=main)](https://github.com/pmodwrc/fits2db/blob/main/.github/workflows/unit_test.yml) [![codecov](https://codecov.io/github/pmodwrc/fits2db/graph/badge.svg?token=92UPKXEOIH)](https://codecov.io/github/pmodwrc/fits2db) [![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)|
| __Package__ | [![PyPI Latest Release](https://img.shields.io/pypi/v/fits2db.svg)](https://pypi.org/project/fits2db/) [![PyPI Downloads](https://img.shields.io/pypi/dm/fits2db.svg?label=PyPI%20downloads)](https://pypi.org/project/fits2db/) |
|__Docs__| [![CI - DOCS](https://img.shields.io/github/actions/workflow/status/pmodwrc/fits2db/build_docs.yml?branch=main)](https://github.com/pmodwrc/fits2db/blob/main/.github/workflows/build_docs.yml) [`Find Here`](https://pmodwrc.github.io/fits2db/)


This is a cli tool to extract table data from a fits file and write it down in a database. 

## Supported databases

| Database   |      Supported      |
|----------|:-------------:|
| MySql & MariaDB|  YES |
| DuckDB | In progress |
| Postgres |  under validation |

## Installation 
For installation up to version 0.0.3 can be installed with pip
```bash 
pip install fits2db
```
For newer verions use the git repository
```bash
pip install git+https://github.com/pmodwrc/fits2db.git@main
```
check if you got the right version with 
```bash 
fits2db --version
```
To init a config file run 
```bash 
fits2db init
```
In the `config.yml` file you now can change the variables needed. 

Fill in the database credentials:
```yaml
database:
  type: mysql
  host: localhost
  user: user
  password: password
  db_name: test_db
  port: 3306
```
and add some paths for your fits files

```yaml
fits_files:
  paths:
    - path/to_your_file/2021-07-07_L1a.fits
    - path_to_your_folder

# Delete rows from above listed files from tables which are not listed below
delete_rows_from_missing_tables: True

tables:
    - name: HOUSEKEEPING
      date_column: timestamp # This column will be interpreted as a datetime variable
    - name: OTHER_TABLE # If no table name given it will use the orignal name
```

Build your database from config file 
```bash 
fits2db build <path_to_config_yaml>
```
This will create the following tables:
| Table   |      Description      |
|----------|:-------------:|
| FITS2DB_META|  Contain meta information about loaded files |
| FITS2DB_TABLE_META | Contains info about all loaded tables from the files |
| HOUSEKEEPING |  Contains the data of your fits files tables HOUSEKEEPING  merged |
| HOUSEKEEPING_META |  Contains the Column information from the fits files|
| OTHER_TABLE |   Contains the data of your fits files tables HOUSEKEEPING  merged|
| OTHER_TABLE_META |  Contains the Column information from the fits files|

To add new Files to a existing database use
```
fits2db update <path_to_config_yaml>
```
Files which are not yet in the database are added. 
Already exisitng files are only updated, if their last change time is newer than
the already existing one.
To force the update of already uploaded files use
```
fits2db update <path_to_config_yaml> -f
```