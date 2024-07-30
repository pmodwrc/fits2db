"""Core module to extract fits files and insert into db"""

from ..fits import FitsFile
from ..config import get_configs
import os
from pathlib import Path
from tqdm import tqdm
from hashlib import sha256
import pandas as pd
from ..adapters import DBWriter
import logging

# Use the configured logger
log = logging.getLogger('fits2db')

def get_all_fits(paths: list)->list:
    """Searches recursive throught all folders of given list of paths for 
    fits files and gives them back.
    Args:
        paths (list): A list of paths to search recursivly for fits files

    Returns:
        list: Returns list of absolute paths of all fits files
    """
    all_fits_files = []
    for path in paths:
        if os.path.isdir(path):
            for root, _, files in os.walk(path):
                for file in files:
                    if file.endswith(".fits"):
                        all_fits_files.append(os.path.join(root, file))
        elif os.path.isfile(path) and path.endswith(".fits"):
            all_fits_files.append(path)
    return all_fits_files


def flatten_and_deduplicate(input_list):
    unique_values = set()
    flat_list = []

    def flatten(item):
        if isinstance(item, list):
            for sub_item in item:
                flatten(sub_item)
        else:
            if item not in unique_values:
                unique_values.add(item)
                flat_list.append(item)

    flatten(input_list)
    return flat_list


class Fits2db:
    def __init__(self, config_path):
        self.config_path = Path(config_path)
        self.configs = get_configs(config_path)
        self.fits_file_paths = self.get_file_names()

    def get_file_names(self) -> list:
        """Return list of all absolute filepaths found from sourced
        given in config file

        Returns:
            list: List of absolute paths
        """
        paths = self.configs["fits_files"]["paths"]
        log.debug(f"paths {paths}")
        log.info("run function")
        return list(dict.fromkeys(get_all_fits(paths)))

    def get_table_names(self):
        self.all_table_names = []
        self.file_table_dict = {}
        for path in tqdm(self.fits_file_paths):
            path = Path(path)
            try:
                file = FitsFile(path)
                self.all_table_names.append(file.table_names)
                self.file_table_dict[path] = file.table_names
            except ValueError as err:
                log.error(err)

        self.all_table_names = flatten_and_deduplicate(self.all_table_names)
        return self.all_table_names, self.file_table_dict

    def create_table_matrix(self, output_format=None, output_file=None):
        all_table_names, file_table_dict = self.get_table_names()
        file_names = [path.name for path in file_table_dict.keys()]
        df = pd.DataFrame(index=file_names, columns=all_table_names)
        for path, tables in file_table_dict.items():
            file_name = path.name
            for table in tables:
                df.at[file_name, table] = "X"

        df = df.fillna("")

        if output_format and file_name:
            current_dir = os.getcwd()
            full_file_path = os.path.join(current_dir, output_file)
            if output_format.lower() == "csv":
                df.to_csv(full_file_path)
            elif output_format.lower() == "excel":
                df.to_excel(full_file_path, index=True)

        return df

    def sha256sum(filename, bufsize=128 * 1024):
        h = sha256()
        buffer = bytearray(bufsize)
        # using a memoryview so that we can slice the buffer without copying it
        buffer_view = memoryview(buffer)
        with open(filename, "rb", buffering=0) as f:
            while True:
                n = f.readinto(buffer_view)
                if not n:
                    break
                h.update(buffer_view[:n])
        return h.hexdigest()

    def upsert_to_db(self):
        for path in tqdm(self.fits_file_paths):
            path = Path(path)
            try:
                file = FitsFile(path)
                writer = DBWriter(self.configs, file)
                writer.upsert()

            except ValueError as err:
                log.error(err)
