"""
This module provides the DBWriter class, which manages database operations
for FITS files using a configurable loader such as MySQL. It supports operations
like upsert, update, and database cleaning.

Classes:
    DBWriter: Handles database operations for FITS files based on the provided configuration.
"""

import logging
from typing import Optional

from pandas import DataFrame

from ..config.config_model import ConfigType
from ..fits import FitsFile
from .mysql import MySQL

# Use the configured log
log = logging.getLogger("fits2db")


class DBWriter:
    """
    Handles database operations for FITS files based on the provided configuration.

    Attributes:
        file (FitsFile): FITS file to be processed.
        config (ConfigType): Configuration settings for the database.
        db_type (Optional[str]): The type of database (e.g., "mysql").
        loader (Optional[MySQL]): The database loader instance.
    """

    def __init__(self, config: ConfigType, file: FitsFile = None) -> None:
        """
        Initializes the DBWriter class.

        Args:
            config (ConfigType): Configuration settings for the database.
            file (FitsFile): FITS file to be processed.
        """
        log.debug("Initializing DBWriter.")
        self.file: FitsFile = file
        self.config: ConfigType = config
        self.db_type: Optional[str] = None
        self.loader = self._load_db()
        log.info("DBWriter initialized successfully.")

    def _get_loader(self) -> Optional[MySQL]:
        """
        Returns the database loader based on the configuration.

        Returns:
            Optional[MySQL]: An instance of the MySQL loader if the
                    database type is MySQL, otherwise None.
        """
        log.debug("Getting database loader for type: %s", self.db_type)
        if self.db_type and self.db_type.lower() == "mysql":
            log.info("MySQL loader created.")
            return MySQL(self.config, self.file)

        log.debug("No loader created. Database type is not MySQL.")
        return None

    def _load_db(self) -> Optional[MySQL]:
        """
        Loads the database type from the configuration and initializes the loader.

        Returns:
            Optional[MySQL]: An instance of the loader based on the database type.
        """
        try:
            self.db_type = self.config["database"]["type"]
            log.debug("Database type loaded: %s", self.db_type)
            loader = self._get_loader()
            if loader:
                log.info("Loader initialized successfully.")
            else:
                log.warning("Loader initialization failed.")
            return loader
        except KeyError as e:
            log.error("Configuration key error: %s", e)
            return None

    def clean_db(self) -> None:
        """
        Deletes all tables created by FITS2DB in the database.
        """
        log.debug("Starting db cleaning operation.")
        try:
            if self.loader:
                self.loader.clean_db()
                log.info("DB clean operation completed successfully.")
            else:
                log.error("Loader is not initialized.")
        except Exception as e:
            log.error(f"Error during upsert operation: {e}")

    def get_db_file_infos(self) -> Optional[DataFrame]:
        """
        Retrieves file information from the FITS2DB_META table.

        Returns:
            Optional[DataFrame]: A DataFrame containing file information from
                    the database, or None if an error occurs.
        """
        log.debug("Starting db cleaning operation.")
        try:
            if self.loader:
                df = self.loader.get_fits2db_meta()
                log.info("FITS2DB_META loaded")
                return df
            else:
                log.error("Loader is not initialized.")
        except Exception as e:
            log.error(f"Error during upsert operation: {e}")

    def upsert(self) -> None:
        """
        Inserts or updates data in the database.
        """
        log.debug("Starting upsert operation.")
        try:
            if self.loader:
                self.loader.upload_file()
                log.info("Upsert operation completed successfully.")
                self.loader.close_connection()
                log.info("Connection closed")
            else:
                log.error("Loader is not initialized.")
        except Exception as e:
            log.error(f"Error during upsert operation: {e}")

    def update(self) -> None:
        """
        Updates data in the database and closes the connection.
        """
        log.debug("Starting update operation.")
        try:
            if self.loader:
                self.loader.update_file()
                log.info("Update operation completed successfully.")
                self.loader.close_connection()
                log.info("Connection closed")
            else:
                log.error("Loader is not initialized.")
        except Exception as e:
            log.error(f"Error during update operation: {e}")
