"""Core module to extract fits files and insert into db"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
from tqdm import tqdm

from ..adapters import DBWriter
from ..config import get_configs
from ..fits import FitsFile

# Use the configured logger
log = logging.getLogger("fits2db")


def get_all_fits(paths: list) -> list:
    """Searches recursive throught all folders of given list of paths for fits files,
     and gives them back.
    Args:
        paths (list): A list of paths to search recursivly for fits files.

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


def flatten_and_deduplicate(input_list: List[Any]) -> List[Any]:
    """Flattens a nested list and removes duplicate values.

    Args:
    ----
        input_list (List[Any]): A potentially nested list of items.

    Returns:
    -------
        List[Any]: A flattened list containing unique items in the order they first appear.
    """
    unique_values = set()
    flat_list = []

    def flatten(item: Any):
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
    """
    A class to manage loading and interacting with FITS files in a SQL database.

    This class handles configuration, file discovery, and database operations
    related to FITS files, making it easy to integrate FITS data with a SQL database.
    """

    def __init__(self, config_path: str):
        """
        Initialize the Fits2db class with a path to the configuration file.

        Args:
            config_path (str): Path to the configuration file.
        """
        self.config_path = Path(config_path)
        self.configs = get_configs(config_path)
        self.fits_file_paths = self.get_file_names()

    def get_file_names(self) -> list[str]:
        """
        Return a list of all absolute file paths found in the sources specified in the config file.

        Returns:
            List[str]: A list of absolute paths to the FITS files.
        """
        paths = self.configs["fits_files"]["paths"]
        log.debug(f"paths {paths}")
        log.info("run function")
        return list(dict.fromkeys(get_all_fits(paths)))

    def get_file_infos(self) -> pd.DataFrame:
        """
        Generate metadata for each FITS file, including filename, path, and last modification date.

        Returns:
            pd.DataFrame: A DataFrame containing metadata for each FITS file.
        """
        meta = []
        for path in self.fits_file_paths:
            path = Path(path)
            absolute_path = path.resolve()
            file_meta = {
                "filename": path.name,
                "filepath": absolute_path.as_posix(),
                "last_file_mutation": datetime.fromtimestamp(
                    os.path.getmtime(absolute_path)
                ),
            }
            meta.append(file_meta)
        df = pd.DataFrame(meta)
        log.debug(df)
        return df

    def get_table_names(self) -> Tuple[List[str], Dict[Path, List[str]]]:
        """
        Retrieve table names from each FITS file.

        Returns:
            Tuple[List[str], Dict[Path, List[str]]]: A tuple containing,
                a list of all unique table names and a dictionary mapping
                file paths to their respective tables.
        """
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

    def create_table_matrix(
        self,
        output_format: Optional[str] = None,
        output_file: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        Create a matrix showing the presence of tables in each FITS file.

        Args:
            output_format (Optional[str]): The format in which to save the matrix ('csv' or 'excel').
            output_file (Optional[str]): The name of the file to save the matrix.

        Returns:
            pd.DataFrame: A DataFrame showing which tables are present in which FITS files.
        """
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

    def build(self, reset: bool = True) -> None:
        """
        Build the database from the FITS files, optionally resetting the database first.

        Args:
            reset (bool): Whether to reset the database before building.
        """
        while True:
            user_input = input(f"This will remove all tables from the database '{self.configs['database']['db_name']}'.\nDo you want to continue? (yes/no): ")
            if user_input.lower() in ["yes", "y"]:
                print("Continuing...")
                break
            elif user_input.lower() in ["no", "n"]:
                print("Exiting...")
                return
            else:
                print("Invalid input. Please enter yes/no.")
        log.debug(f"Start building db with reset = {reset}")
        writer = DBWriter(self.configs)
        if reset:
            writer.clean_db()
            log.debug("Clean db success start uploading files")
        for path in tqdm(self.fits_file_paths):
            path = Path(path)
            try:
                file = FitsFile(path)
                writer = DBWriter(self.configs, file)
                writer.upsert()

            except ValueError as err:
                log.error(f"\n {err}")

    def get_db_diff(self, force=False) -> None:
        """
        Compare file metadata with database entries to find new or updated files.
        """
        self.file_infos['last_file_mutation'] = self.file_infos['last_file_mutation'].dt.round('s')
        merged_df = pd.merge(
            self.file_infos,
            self.db_file_infos,
            on=["filename", "filepath"],
            how="left",
            suffixes=("_file", "_db"),
        )

        new_files = merged_df[merged_df["last_file_mutation_db"].isna()]
        if force:
            files2update = merged_df[merged_df["last_file_mutation_db"].notna()]
        else:
            files2update = merged_df[
                (
                    merged_df["last_file_mutation_file"]
                    > merged_df["last_file_mutation_db"]
                )
            ]
        self.new_files = new_files[
            ["filename", "filepath", "last_file_mutation_file"]
        ].rename(columns={"last_file_mutation_file": "last_file_mutation"})
        self.files2update = files2update[
            ["filename", "filepath", "last_file_mutation_file"]
        ].rename(columns={"last_file_mutation_file": "last_file_mutation"})

    def update_db(self, force=False) -> None:
        """
        Update the database with new or modified FITS files.
        """
        self.file_infos = self.get_file_infos()
        log.info(self.file_infos)
        writer = DBWriter(self.configs)
        self.db_file_infos = writer.get_db_file_infos()
        log.info(self.db_file_infos)
        self.get_db_diff(force=force) # TODO Make sideeffects of function clear!!

        fits_file_paths = self.new_files["filepath"].to_list()
        for path in tqdm(fits_file_paths, desc="Upload new files"):
            path = Path(path)
            try:
                file = FitsFile(path)
                writer = DBWriter(self.configs, file)
                writer.upsert()

            except ValueError as err:
                log.error(f"\n {err}")

        fits_file_paths = self.files2update["filepath"].to_list()
        for path in tqdm(fits_file_paths, desc="Update files"):
            path = Path(path)
            try:
                file = FitsFile(path)
                writer = DBWriter(self.configs, file)
                writer.update()

            except ValueError as err:
                log.error(f"\n {err}")

    def upsert_to_db(self) -> None:
        """
        Insert or update all FITS files into the database, resetting the database first.
        """
        log.debug("Start upsert to db")
        writer = DBWriter(self.configs)
        writer.clean_db()
        log.debug("Clean db success start uploading files")
        for path in tqdm(self.fits_file_paths):
            path = Path(path)
            try:
                file = FitsFile(path)
                writer = DBWriter(self.configs, file)
                writer.upsert()

            except ValueError as err:
                log.error(f"\n {err}")
