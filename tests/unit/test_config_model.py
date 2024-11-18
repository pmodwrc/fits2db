import pytest
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from pydantic import ValidationError
from fits2db.config.config_model import (
    DatabaseConfig,
    ApplicationConfig,
    FitsConfig,
    ConfigFileValidator,
)

ACCEPTABLE_TYPES = {"mysql"}


def test_valid_database_config_user_password():
    config = DatabaseConfig(
        type="mysql",
        host="localhost",
        user="admin",
        password="adminpass",
        token=None,
        port=3306,
    )
    assert config.user == "admin"
    assert config.password == "adminpass"


def test_valid_database_config_token():
    config = DatabaseConfig(
        type="mysql",
        host="localhost",
        user=None,
        password=None,
        token="sometoken",
        port=3306,
    )
    assert config.token == "sometoken"


def test_invalid_database_config_no_credentials():
    with pytest.raises(ValidationError):
        DatabaseConfig(
            type="mysql",
            host="localhost",
            user=None,
            password=None,
            token=None,
            port=3306,
        )


def test_invalid_database_config_both_credentials():
    with pytest.raises(ValidationError):
        DatabaseConfig(
            type="mysql",
            host="localhost",
            user="admin",
            password="adminpass",
            token="sometoken",
            port=3306,
        )


def test_invalid_database_type():
    with pytest.raises(ValidationError):
        DatabaseConfig(
            type="sqlite",
            host="localhost",
            user="admin",
            password="adminpass",
            token=None,
            port=3306,
        )


def test_valid_application_config():
    db_config = DatabaseConfig(
        type="mysql",
        host="localhost",
        user="admin",
        password="adminpass",
        token=None,
        port=3306,
    )
    paths = [r"tests\unit\data\test.fits", r"tests\unit\data"]
    tables = [
        {"name": "test", "ingest_all_columns": True},
        {"name": "test2", "ingest_all_columns": False},
    ]
    fits_config = FitsConfig(paths=paths, tables=tables)
    app_config = ApplicationConfig(database=db_config, fits_files=fits_config)
    assert app_config.database.host == "localhost"
    assert app_config.fits_files.paths == [
        r"tests\unit\data\test.fits",
        r"tests\unit\data",
    ]
    assert app_config.fits_files.tables[0].model_dump() == {
        "columns": None,
        "date_column": None,
        "description": None,
        "name": "test",
        "ingest_all_columns": True,
    }


def test_invalid_application_config():
    with pytest.raises(ValidationError):
        FitsConfig(name=123)


def test_config_file_validator_existing_file():
    # Create a temporary file to test with
    with NamedTemporaryFile(delete=False) as temp_file:
        temp_file_path = temp_file.name

    try:
        config = ConfigFileValidator(path=temp_file_path)
        assert config.path == Path(temp_file_path)
    finally:
        # Clean up the temporary file
        os.remove(temp_file_path)


def test_config_file_validator_non_existing_file():
    with pytest.raises(ValidationError):
        ConfigFileValidator(path="non_existing_file.txt")


def test_config_file_validator_directory_instead_of_file():
    with pytest.raises(ValidationError):
        ConfigFileValidator(
            path=os.getcwd()
        )  # Using current working directory


def test_config_file_validator_empty_path():
    with pytest.raises(ValidationError):
        ConfigFileValidator(path="")
