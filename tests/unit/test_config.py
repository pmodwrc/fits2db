import pytest
import os
import yaml
from fits2db.config import get_configs, generate_config
from fits2db.config.config import render_template
from unittest.mock import patch, mock_open, MagicMock
from jinja2 import Environment, FileSystemLoader
from pydantic import ValidationError

current_dir = os.path.dirname(__file__)
sample_config_file = os.path.join(current_dir, "data", "config.yaml")
sample_invalid_config_file = os.path.join(
    current_dir, "data", "invalid_config.yaml"
)
sample_invalid_yml_file = os.path.join(
    current_dir, "data", "invalid_config_yaml.yaml"
)
mock_log = MagicMock()


def test_get_configs_valid():
    """Test getting a valid config file"""
    configs = get_configs(sample_config_file)
    assert configs["database"]["type"] == "mysql"


def test_get_configs_invalid():
    """Test getting a invalid config file"""
    with pytest.raises(ValueError):
        configs = get_configs(sample_invalid_config_file)
    # assert configs == {}


def test_get_configs_invalid_yml():
    """Test getting a invalid yml file"""
    # with pytest.raises(ValidationError):
    #    get_configs(sample_invalid_yml_file)
    with pytest.raises(yaml.YAMLError):
        configs = get_configs(sample_invalid_yml_file)
    # assert configs == {}


def test_render_template():
    """Test render template"""


@patch("builtins.open", new_callable=mock_open)
@patch("os.path.isdir")
@patch("fits2db.config.config.render_template")
def test_generate_config_file_success(
    mock_render_template, mock_isdir, mock_file_open
):
    # Mock the behavior of render_template with expected content
    expected_content = """database:
  type: mysql
  host: localhost
  user: db_user
  password: user_password
  token: 
  port: 3006

fits_files:
  name: path_to_fits_file
"""
    mock_render_template.return_value = expected_content

    # Test when path is a directory
    mock_isdir.return_value = True
    path = "mock_dir"
    result = generate_config(path)

    # Check if the file was created with the correct name in the directory
    mock_file_open.assert_called_once_with(
        os.path.join(path, "config.yml"), "w", encoding="utf-8"
    )
    mock_file_open().write.assert_called_once_with(expected_content)
    assert result

    # Reset mocks for next test
    mock_file_open.reset_mock()

    # Test when path is a file
    mock_isdir.return_value = False
    path = "mock_file.yml"
    result = generate_config(path)

    # Check if the file was created with the specified name
    mock_file_open.assert_called_once_with(path, "w", encoding="utf-8")
    mock_file_open().write.assert_called_once_with(expected_content)
    assert result


@patch("builtins.open", new_callable=mock_open)
@patch("os.path.isdir")
@patch("fits2db.config.config.render_template")
def test_generate_config_failure(
    mock_render_template, mock_isdir, mock_file_open
):
    mock_render_template.return_value = "mocked config content"
    mock_isdir.return_value = False
    path = "invalid_path.txt"

    result = generate_config(path)
    assert not result


def test_render_template_basic():
    template_name = "test_template.html"
    context = {"key": "value"}

    # Mocking the environment and template
    with patch("fits2db.config.config.Environment") as MockEnvironment:
        mock_env = MockEnvironment.return_value
        mock_template = mock_env.get_template.return_value
        mock_template.render.return_value = "rendered content"

        # Mock the logger
        with patch("fits2db.config.config.log", mock_log):
            rendered_content = render_template(template_name, context)

            # Basic assertion to check if the rendered content is correct
            assert rendered_content == "rendered content"

            # Ensure the template was fetched with the correct name
            mock_env.get_template.assert_called_with(template_name)

            # Ensure the template was rendered with the correct context
            mock_template.render.assert_called_with(context)


def test_render_template_empty_context():
    template_name = "test_template.html"
    context = {}

    # Mocking the environment and template
    with patch("fits2db.config.config.Environment") as MockEnvironment:
        mock_env = MockEnvironment.return_value
        mock_template = mock_env.get_template.return_value
        mock_template.render.return_value = "rendered with empty context"

        # Mock the logger
        with patch("fits2db.config.config.log", mock_log):
            rendered_content = render_template(template_name, context)

            # Basic assertion to check if the rendered content is correct
            assert rendered_content == "rendered with empty context"

            # Ensure the template was fetched with the correct name
            mock_env.get_template.assert_called_with(template_name)

            # Ensure the template was rendered with the correct context
            mock_template.render.assert_called_with(context)


def test_render_template_file_not_found():
    template_name = "non_existent_template.html"
    context = {"key": "value"}

    # Mocking the environment to raise TemplateNotFound error
    with patch("fits2db.config.config.Environment") as MockEnvironment:
        mock_env = MockEnvironment.return_value
        mock_env.get_template.side_effect = Exception("Template not found")

        # Mock the logger
        with patch("fits2db.config.config.log", mock_log):
            with pytest.raises(Exception, match="Template not found"):
                render_template(template_name, context)

            # Ensure the template was attempted to be fetched
            mock_env.get_template.assert_called_with(template_name)
