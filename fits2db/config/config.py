"""
This module contains the configuration validation for the FITS to database application.
"""

from .config_model import ConfigFileValidator, ApplicationConfig, ConfigType

from typing import Union
import yaml
import os
from jinja2 import Environment, FileSystemLoader


def get_configs(path: Union[str, os.PathLike]) -> ConfigType:
    """_summary_

    Args:
        path (Union[str, os.PathLike]): Path to config yaml file

    Returns:
        ConfigType: Data from config file loaded and validated
    """
    config_validator = ConfigFileValidator(path=path)
    with open(config_validator.path, "r", encoding="utf-8") as file:
        config_data = yaml.safe_load(file)
    try: 
        data = ApplicationConfig(**config_data).model_dump()
    except Exception as err:
        print('Config file error:', err)
        data = {}
    return data


def render_template(template_name, context):
    template_path = os.path.join(os.path.dirname(__file__), 'templates')
    env = Environment(loader=FileSystemLoader(template_path))
    template = env.get_template(template_name)
    return template.render(context)

def generate_config():    
    config_content = render_template('config.yaml.j2', {'db_type': "mysql"})
    with open(os.path.join('config.yaml'), 'w') as f:
        f.write(config_content)
    

