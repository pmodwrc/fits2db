"""FitsFile class to get the data"""

from dataclasses import dataclass, field
from itertools import count
from datetime import datetime
from astropy.io import fits
import pandas as pd
import os
import time
from typing import TypedDict, List
from pathlib import Path


counter = count()


@dataclass
class FitsTable:
    name: str
    meta: pd.DataFrame
    data: pd.DataFrame
    create_at: datetime = field(default_factory=datetime.now)
    index: int = field(default_factory=lambda: next(counter))


@dataclass
class FitsFile:
    file_path: Path
    absolute_path: Path = field(init=False)
    file_name: str = field(init=False)
    file_size: int = field(init=False)
    hdul: fits.HDUList = field(init=False)
    table_names: List = field(init=False)
    config: dict = field(init=False)

    def __post_init__(self):
        self.check_path()
        self.load_file()
        self.get_table_names()
        self.mtime = time.ctime(os.path.getmtime(self.absolute_path))
        self.mdate = datetime.fromtimestamp(
            os.path.getmtime(self.absolute_path)
        )

    def check_path(self):
        if not self.file_path.exists():
            raise FileNotFoundError(
                f"The file {self.file_path} does not exist."
            )
        if not self.file_path.is_file():
            raise ValueError(f"The path {self.file_path} is not a file.")

        self.absolute_path = self.file_path.resolve()
        self.file_name = self.file_path.name
        self.file_size = self.file_path.stat().st_size

    def load_file(self):
        if self.file_path.suffix.lower() != ".fits":
            raise ValueError(f"The file {self.file_path} is not a FITS file.")
        try:
            self.hdul = fits.open(self.absolute_path, memmap=True)
        except Exception as e:
            raise ValueError(
                f"The file {self.file_path} is not a valid FITS file: {e}"
            )

    def get_table(self, name: str) -> FitsTable:
        """Access a specific table by index without loading all tables into memory."""
        if name not in self.table_names:
            raise KeyError(
                f"\n Key {name} is not a table in HDUL. \n in file {self.absolute_path}"
            )
        hdu = self.hdul[name]
        data = self.extract_data(hdu)
        meta = self.extract_meta(hdu)
        fits_table = FitsTable(name=name, data=data, meta=meta)
        return fits_table

    def get_table_names(self):
        """Return the names of all tables in the FITS file."""
        self.table_names = [
            hdu.name
            for hdu in self.hdul
            if isinstance(hdu, (fits.BinTableHDU, fits.TableHDU))
        ]

    def close(self):
        """Close the FITS file."""
        if hasattr(self, "hdul") and self.hdul:
            self.hdul.close()
            self.hdul = None

    def __del__(self):
        """Ensure resources are freed when the object is deleted."""
        self.close()

    def extract_data(self, hdu: fits.Card) -> pd.DataFrame:
        data = hdu.data
        # Convert all big-endian columns to little-endian
        columns = data.columns.names
        little_endian_data = {
            col: data[col].byteswap().newbyteorder()
            if data[col].dtype.byteorder == ">"
            else data[col]
            for col in columns
        }
        df = pd.DataFrame(little_endian_data)
        return df

    def extract_meta(self, hdu: fits.Card) -> pd.DataFrame:
        return pd.DataFrame(
            list(hdu.header.items()), columns=["Keyword", "Value"]
        )
