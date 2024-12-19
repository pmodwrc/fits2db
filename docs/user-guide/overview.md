# fits2db User Guide
## Overview
`fits2db` is a command-line interface (CLI) tool designed to load and update tables from FITS (Flexible Image Transport System) files into an SQL database. This tool is particularly useful for managing large datasets in astronomy and other fields that utilize FITS files for data storage.

### Key Features

- Load FITS file data into SQL databases.
- Automatically create and initialize database tables based on FITS file contents.
- Append new data and update existing entries efficiently.
- Maintain metadata tables describing the columns and FITS file information.

### Installation
To install fits2db, follow these steps:

1. Dependencies: Ensure you have Python installed on your system along with necessary libraries. You might need libraries like astropy for handling FITS files and SQLAlchemy for database interactions.

2. Install fits2db:

```bash title="pip installation"
pip install fits2db
```

### Configuration
Before using fits2db, you need to create a configuration yaml file. This file contains information about your database and the FITS files you want to use.
??? note "Example config file"
    Example config file
    ```yaml title="Example yaml"
    # Your db configs:
    database:
    type: mysql
    host: localhost
    user: user
    password: userpassword
    db_name: fitsdata
    port: 3306

    # Your fits files
    fits_files:
    paths:
        - tests\unit\data\2021-07-07_L1a.fits
        - test\unit\data # If just a path is given it will search recursive for fits files
    
    delete_rows_from_missing_tables: False # [optional] by default false

    tables: # The tables from the fitsfiles you want to upload
        - name: HOUSEKEEPING
          date_column: timetsamp
        - name: JTSIM_BROADCAST
          date_column: timestamp

    ```
### Configuration Parameters

- database: Specifies the type and name of your database.
    - type: Type of database (currently just mysql).
    - host: Db host
    - user: User of db that has rights to read write create and drop tables
    - password: pw of user
    - port: default is 3306 if not specified

- fits_files: A list of directories or paths containing your FITS files.
    - path: Path to the directory with FITS files.
    - tables: Names of the tables to create and populate in the database.

## Usage
### Initial Setup

To initialize the database and load data from the FITS files, use the rebuild command. This command creates the necessary tables in the SQL database and populates them with data from the FITS files.

## Additional Resources

- [FITS File Format Documentation](https://fits.gsfc.nasa.gov/fits_documentation.html)
- [SQLAlchemy Documentation](https://www.sqlalchemy.org/)

## License and Contributions

fits2db is an open-source project licensed under the MIT License. Contributions are welcome! To contribute, follow these steps:

- Fork the repository.
- Create a new branch for your feature or bugfix.
- Submit a pull request with a detailed description of your changes.

For more details, see the [contribution guide](../contribution/contribution.md).