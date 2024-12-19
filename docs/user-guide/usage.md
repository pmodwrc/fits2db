# Usage

## __Getting help__
If you need some information about a command you can always pass the `--help` flag to get some information

## __Generate a config file__
First you can generate a template config file:
```bash
$ fits2db init
```
!!! note
    you can also pass a path to the command to choose where the config file should be generated and what the name of the file should be:

    ```bash
    $ fits2db init <folder_path>
    ```
    this generates a file `config.yml` under your given path
    ```bash
    $ fits2db init <example/path/config_test.yaml>
    ```
    this gernerates the config file with the name `config_test.yaml`.




## __Make your changes__
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

# Delete rows from above listed files from tables which are not listed below. By default False
delete_rows_from_missing_tables: True

tables:
    - name: HOUSEKEEPING
      date_column: timestamp # This column will be interpreted as a datetime variable
    - name: IRRADIANCE # If no table name given it will use the orignal name
      date_column: irradiance_timeutc
```


!!! note
    if a folder is given all fits files under this folder will be taken recursively for upload.

## __Check if the right files are taken__
You can check if you get the right fits files with 
```bash
$ fits2db files <path_to_config_file>
```
this command shows all files it will consider uploading in your terminal and at the end shows the number of files.

!!! note 
     If you don't add an path the cli looks for the config file in the same folder as you are currently in.

## __Inspect available Tables__

If you want to see what tables are available in your fits files you can run 
```bash
$ fits2db tables <path_to_config_file> 
```
this will get you a summary of all tables

!!! tip 
    If you want to see if the tables are available in all files just run the sam command with the matrix flag
    ```bash
    $ fits2db tables <path_to_config_file> -m
    ```
    this will show the reult in the terminal. If you want to have and excel or csv use
    ```bash
    $ fits2db tables <path_to_config_file> -m --excel --filename path/your_filename.xlsx
    ```

## __Build db__

Now upload the data into our data base we use the build command
```bash
$ fits2db build <path_to_config_file> 
```
this will upload all the fits tables into your data base and create the meta tables to keep track on changes of the files

!!! warning
    If you rerun the build command it acts as an reset. it will drop the tables and reupload all data to have a fresh start. This is only recommend to use when you lost track of some changes in the data you have done manually and you are not sure you corrupted the data.


## __Update db__

Once builded and you get new files or changes you can update the database. 
This command will check if there a new files in your defnied folders and 
upload them to the db. If the timestamp of your file changed to a newer
date. Like when you changed a file it will also update this file to the 
newer version. This way the fits files and the db stay in sync. To update just run 

```bash
$ fits2db update <path_to_config_file> 
```
!!! note
    If you want to add new tables from a already updated file, you can use the ```-f``` flag
    to force update all files specified in the config.