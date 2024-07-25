
import pytest
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from pydantic import ValidationError
from fits2db.config.config import get_configs

current_dir = os.path.dirname(__file__)
sample_config_file = os.path.join(current_dir, 'data', 'config.yaml')


def test_get_configs_valid():
    """Test getting a valid config file"""
    configs = get_configs(sample_config_file)
    assert configs["database"]["type"] == "mysql"


