"""
This module defines the BaseLoader class, an abstract base class for handling
the loading of data from FITS files into a database. The class provides
functionality to write metadata about the FITS files and their corresponding
tables into the database and offers abstract methods for custom data
operations such as dropping tables and upserting data.

Classes:
    BaseLoader: An abstract base class for writing data from FITS files into a database.
"""

import logging
from abc import ABC, abstractmethod

import pandas as pd
from sqlalchemy import engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql import select

from ..config.config_model import ConfigType
from ..fits.fits import FitsFile
from .meta import Base, Fits2DbMeta, Fits2DbTableMeta

log = logging.getLogger("fits2db")


class BaseLoader(ABC):
    """
    An abstract base class for writing data from FITS files into a database.

    Attributes:
        db_url (str): The database URL.
        engine (engine.Engine): The SQLAlchemy engine for the database.
        config (ConfigType): Configuration data for loading tables from the FITS file.
        file (FitsFile): The FITS file object containing data to be loaded.
        session (Session): SQLAlchemy session object for database transactions.
        new_file (Fits2DbMeta): Metadata object for the FITS file.
        db_table_names (set): Set of table names currently in the database.
    """

    def __init__(
        self, db_url: str, engine: engine, config: ConfigType, file: FitsFile
    ):
        """
        Initializes the BaseLoader with the given database URL, engine, configuration, and FITS file.

        Args:
            db_url (str): The database URL.
            engine (engine.Engine): The SQLAlchemy engine for the database.
            config (ConfigType): Configuration data for loading tables from the FITS file.
            file (FitsFile): The FITS file object containing data to be loaded.
        """
        self.db_url = db_url
        self.engine = engine
        self.config = config
        self.file = file

    def db_session(self) -> Session:
        """
        Creates and returns a new SQLAlchemy session for the database.

        Returns:
            Session: A new SQLAlchemy session object.
        """
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        return Session()

    def write_file_meta(self) -> None:
        """
        Writes metadata about the FITS file to the database.
        """
        log.debug(f"Filepath {self.file.absolute_path.as_posix()}")
        self.new_file = Fits2DbMeta(
            filename=self.file.file_name,
            filepath=self.file.absolute_path.as_posix(),
            last_file_mutation=self.file.mdate,
        )
        self.session.add(self.new_file)
        self.session.commit()

    def write_table_meta(self, tbl_name: str, df: pd.DataFrame) -> None:
        """
        Writes metadata about a table in the FITS file to the database.

        Args:
            tbl_name (str): The name of the table.
            df (pd.DataFrame): The DataFrame representing the table data.
        """
        rows, cols = df.shape
        new_table = Fits2DbTableMeta(
            file_meta_id=self.new_file.id,
            tablename=tbl_name,
            record_count=rows,
            column_count=cols,
        )
        self.session.add(new_table)
        self.session.commit()

    def get_tables(self) -> None:
        """
        Retrieves and stores the names of all tables currently in the database.
        """
        db_table_names = self.session.execute(
            select(Fits2DbTableMeta.tablename)
        ).fetchall()
        db_table_names = [name[0] for name in db_table_names]
        self.db_table_names = set(db_table_names)

    @abstractmethod
    def drop_tables(self) -> None:
        """
        Drops specific tables from the database. This method must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def drop_meta_tables(self) -> None:
        """
        Drops metadata tables from the database. This method must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def upsert_data_table(
        self, table_name: str, df: pd.DataFrame, unique_key: str
    ) -> None:
        """
        Inserts or updates data in a specific table in the database. This method must be implemented by subclasses.

        Args:
            table_name (str): The name of the table to upsert data into.
            df (pd.DataFrame): The DataFrame containing the data to upsert.
            unique_key (str): The unique key used to identify records for updating.
        """
        pass

    @abstractmethod
    def update_table(
        self, table_name: str, df: pd.DataFrame, unique_key: str
    ) -> None:
        """
        Updates data in a specific table in the database. This method must be implemented by subclasses.

        Args:
            table_name (str): The name of the table to update.
            df (pd.DataFrame): The DataFrame containing the data to update.
            unique_key (str): The unique key used to identify records for updating.
        """
        pass

    def clean_db(self) -> None:
        """
        Cleans the database by dropping specific tables and metadata tables.
        """
        self.session = self.db_session()
        self.get_tables()
        log.info(f"Tables in DB:{self.db_table_names}")
        self.drop_tables()
        self.drop_meta_tables()

    def get_fits2db_meta(self) -> pd.DataFrame:
        """
        Retrieves the FITS2DB_META table from the database and returns it as a DataFrame.

        Returns:
            pd.DataFrame: The DataFrame containing the FITS2DB_META table data.
        """
        try:
            df = pd.read_sql_table("FITS2DB_META", con=self.engine)
            return df
        except Exception as err:
            log.error(err)
            raise

    def upsert_file(self) -> None:
        """
        Upserts the FITS file and its tables into the database.
        """
        self.session = self.db_session()
        self.write_file_meta()
        table_configs = self.config["fits_files"]["tables"]
        log.debug("Start upserting data")

        for table in table_configs:
            log.debug(f"Table in configs: {table}")
            table_name = table["name"]
            log.info(table_name)
            log.info(table["ingest_all_columns"])
            try:
                df = self.file.get_table(table_name)
                df.data["FILE_META_ID"] = self.new_file.id
                df.data.columns = map(str.upper, df.data.columns)
                df.meta.columns = map(str.upper, df.meta.columns)
                self.write_table_meta(table_name, df.data)
                self.upsert_data_table(table_name, df.data)
                self.update_table(table_name + "_META", df.meta)
            except KeyError as err:
                log.error(f"\n {err}")
        self.session.close()

    def update_file(self) -> None:
        """
        Updates the metadata and data of the FITS file in the database.
        """
        self.session = self.db_session()
        file_record = (
            self.session.query(Fits2DbMeta)
            .filter_by(
                filepath=self.file.absolute_path.as_posix(),
                filename=self.file.file_name,
            )
            .first()
        )
        if file_record is None:
            log.error(
                f"No record found for file: {self.file.file_name} at {self.file.absolute_path.as_posix()}"
            )
            return
        file_record.last_file_mutation = self.file.mdate

        self.session.commit()
        log.debug(
            f"Record for file: {self.file.file_name} at {self.file.absolute_path.as_posix()} has been updated"
        )
