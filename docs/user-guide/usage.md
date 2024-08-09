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
and add some paths for your fis files

```yaml
fits_files:
  paths:
    - path/to_your_file/2021-07-07_L1a.fits
    - path_to_your_folder

```
!!! note
    if a folder is given all fits files under this folder will be taken for upload.

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
    