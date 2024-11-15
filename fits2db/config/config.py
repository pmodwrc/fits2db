"""
This module contains the configuration validation for the FITS to database application.
"""

from typing import Union
import yaml
import os
from jinja2 import Environment, FileSystemLoader

from .config_model import ConfigFileValidator, ApplicationConfig, ConfigType
import logging


log = logging.getLogger("fits2db")


def get_configs(path: Union[str, os.PathLike]) -> ConfigType:
    """Loads config file from given path

    Args:
        path (Union[str, os.PathLike]): Path to config yaml file

    Returns:
        ConfigType: Data from config file loaded and validated
    """
    config_validator = ConfigFileValidator(path=path)
    with open(config_validator.path, "r", encoding="utf-8") as file:
        try:
            config_data = yaml.safe_load(file)
        except yaml.YAMLError as err:
            log.error("YAML loading error: %s", err)
            raise
            return {}

    try:
        data = ApplicationConfig(**config_data).model_dump()
    except (TypeError, ValueError) as err:
        log.error("Config file validation error: %s", err)
        raise
        return {}

    return data


def render_template(template_name: str, context: dict) -> str:
    """Renders a given template under the relative template directory

    Args:
        template_name (str): Name of template
        context (dict): Dict with template conext

    Returns:
        str: Rendered template as str
    """
    template_path = os.path.join(os.path.dirname(__file__), "templates")
    log.info(f"Template path: {template_path}")
    env = Environment(loader=FileSystemLoader(template_path))
    template = env.get_template(template_name)
    log.debug(f"Template object: {template}")
    return template.render(context)


def generate_config(path: Union[str, os.PathLike]) -> bool:
    """Generate an example config file"""
    try:
        log.debug(f"Passed path: {path}")
        if os.path.isdir(path):
            log.debug("Path is a directory")
            file_path = os.path.join(path, "config.yml")
            log.info(f"Constructed config file path {file_path}")
        else:
            if path.endswith(".yml") or path.endswith(".yaml"):
                file_path = path
            else:
                raise ValueError(
                    "The path must either be a directory or specify a file ending with '.yml'"
                )

        config_content = render_template(
            "config.yaml.j2", {"db_type": "mysql"}
        )

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(config_content)

        log.info(f"Configuration successfully written to {file_path}")
        return True

    except Exception as e:
        log.error(f"Failed to write configuration file: {e}")
        return False
