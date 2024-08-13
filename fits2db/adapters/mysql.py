"""
This module provides an interface for interacting with a MySQL database using SQLAlchemy.
It includes methods for creating database connections, managing tables, and performing
operations such as upsert and merge.

Classes:
    MySQL: Manages MySQL database operations related to FITS files.
"""

import logging


from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import DATETIME


from ..config.config_model import ConfigType
from ..fits.fits import FitsFile
from .base import BaseLoader

logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
log = logging.getLogger("fits2db")


class MySQL(BaseLoader):
    """
    Handles MySQL database operations for managing FITS files.

    Inherits from:
        BaseLoader: A base class for loading data into databases.

    Attributes:
        config (ConfigType): Configuration details for database connection.
        engine: SQLAlchemy engine connected to the MySQL database.
    """

    def __init__(self, config: ConfigType, file: FitsFile) -> None:
        """
        Initializes the MySQL class with database configuration and a FITS file.

        Args:
            config (ConfigType): Configuration details for database connection.
            file (FitsFile): FITS file to be processed.
        """
        self.config = config
        db_url = self.create_db_url()
        engine = create_engine(db_url)
        super().__init__(db_url, engine, config, file)

    def create_db_url(self) -> str:
        """
        Creates a database connection URL from the configuration.

        Returns:
            str: Connection URL for MySQL.
        """
        log.debug("Start create db url")
        user = self.config["database"]["user"]
        password = self.config["database"]["password"]
        host = self.config["database"]["host"]
        port = self.config["database"]["port"]
        db_name = self.config["database"]["db_name"]
        url = (
            f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db_name}"
        )
        log.debug("Created url")
        log.info(url)
        return url
