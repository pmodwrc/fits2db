import pytest
from astropy.io import fits
from pathlib import Path
import pandas as pd
from fits2db.fits import FitsFile

# Sample FITS file paths for testing
SAMPLE_FITS_FILE = Path(r"data\2021-07-07_L1a.fits")
SAMPLE_NON_FITS_FILE = Path(r"sample.txt")
SAMPLE_TABLE_NAME = "CONTROL_NORMAL"
NON_EXISTENT_FILE = Path("non_existent.fits")


@pytest.fixture
def create_sample_fits_file(tmp_path):
    """Create a sample FITS file for testing."""
    file_path = tmp_path / "sample.fits"
    col1 = fits.Column(name="col1", format="E", array=[1.0, 2.0, 3.0])
    col2 = fits.Column(name="col2", format="E", array=[4.0, 5.0, 6.0])
    cols = fits.ColDefs([col1, col2])
    hdu = fits.BinTableHDU.from_columns(cols)
    hdu.name = SAMPLE_TABLE_NAME
    hdu.writeto(file_path)
    return file_path


@pytest.fixture
def fits_file(create_sample_fits_file):
    return FitsFile(file_path=create_sample_fits_file)


def test_get_table_valid(fits_file):
    """Test getting a valid table from the FITS file."""
    table = fits_file.get_table(SAMPLE_TABLE_NAME)
    assert table.name == SAMPLE_TABLE_NAME
    assert isinstance(table.data, pd.DataFrame)
    assert isinstance(table.meta, pd.DataFrame)


def test_get_table_invalid_table_name(fits_file):
    """Test getting a table with an invalid name from the FITS file."""
    with pytest.raises(KeyError):
        fits_file.get_table("INVALID_TABLE")


def test_get_table_names(fits_file):
    """Test the table names extraction from the FITS file."""
    assert SAMPLE_TABLE_NAME in fits_file.table_names


def test_check_path_non_existent_file():
    """Test the check_path method with a non-existent file."""
    with pytest.raises(FileNotFoundError):
        FitsFile(file_path=NON_EXISTENT_FILE)


def test_check_path_non_file(tmp_path):
    """Test the check_path method with a path that is not a file."""
    non_file_path = tmp_path / "non_file_dir"
    non_file_path.mkdir()
    with pytest.raises(ValueError):
        FitsFile(file_path=non_file_path)


def test_load_file_invalid_format(tmp_path):
    """Test the load_file method with a non-FITS file."""
    invalid_file_path = tmp_path / SAMPLE_NON_FITS_FILE
    invalid_file_path.write_text("This is not a FITS file.")
    with pytest.raises(ValueError):
        FitsFile(file_path=invalid_file_path)
