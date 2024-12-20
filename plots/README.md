# Requirements
The script was written using python3.11
The required packages can be installed using 
```
pip install -r requirements.txt
```

# Plot Usage

Plot data by using the `plot_data.py` script.
Parameters:
| Parameter  | key         | Description | Standard value
| ---------- | ----------- | ----------- | ---------------
| DB Config | `-c` | Path to config file that contains the Database Connection Informations | `./db_conf.yaml`
|  Mode  | -  | Plot mode (Daily, monthly, ...) | -
| Start Date  | `-s`  | Start date in format yyyy-mm-dd, if monthly the day can be discarded and if yearly, the day and month can be discarded. | -
| End Date | `-e` | End date in the same format as the start date. If no end date is set, a single plot with the start date is made. | -
| Save directory | `-d` | Directory in which the plots are saved to. This directory must already exist before running the script. | `./plots/`
| Add Irradiance | `--add_irradiance` | Boolean flag, if it is set, the Irradiance data is also plotted. If mode is `lifetime` then irradiance is plotted either way. | `False`
| Add Parameter | `--add_parameter` | Boolean flag, if it is set, the Parameter data is also plotted. If mode is `lifetime` then parameters are plotted either way. | `False`

The lifetime plot only accepts the optional parameters for the db config and save directory

## DB Config
The Database Config file must contain the following variables:
- type, eg. mysql
- host, eg. localhost
- user, eg. db_user
- password 
- port, eg 3306
- db_name, eg fistdb

## Examples:

### Daily Plot

Plot daily plots from the 2nd of march to the 12th of march. The plots are saved into the standard ./plots/ directory.
```
python plot_data.py daily -s 2024-03-02 -e 2024-03-12
```

### Monthly Plot
Plot monthly plots from March 2023 to October 2023 into the monthly directory
```
python plot_data.py monthly -s 2023-03 -e 2023-10 -d ./monthly/
```

### Anual Plot
Anual plots for the years 2022, 2023, 2024
```
python plot_data.py monthly -s 2022 -e 2024
```

### Lifetime
Plot Lifetime plots. Since the lifetime plots over the whole range, no start or end date is needed.
```
python plot_data.py lifetime 
```

### Custom
With the custom mode, plots between any two dates can be generated.
Eg between the first Januari and the ninth April in 2023.
```
python plot_data.py custom -s 2023-01-01 -e 2023-04-09 
```

### Different db_config
To use a different db config, it must be added before the mode descriptor.
```
python plot_data.py -c ./configs/db.yaml monthly -s 2022-10 -e 2023-04
```
