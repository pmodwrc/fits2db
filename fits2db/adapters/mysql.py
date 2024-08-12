"""
This module provides an interface for interacting with a MySQL database using SQLAlchemy.
It includes methods for creating database connections, managing tables, and performing
operations such as upsert and merge.

Classes:
    MySQL: Manages MySQL database operations related to FITS files.
"""

import logging
from typing import Any, Dict

import pandas as pd
from sqlalchemy import MetaData, Table, create_engine, exc, text
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.exc import SQLAlchemyError


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

    def drop_tables(self) -> None:
        """
        Drops FITS2DB created data tables from the database if they exist.
        """
        metadata = MetaData()
        metadata.reflect(bind=self.engine)
        log.info(metadata.tables)
        for table_name in self.db_table_names:
            if table_name in metadata.tables:
                metadata.tables[table_name].drop(self.engine)
                log.info(f"Dropped table {table_name}")
            if table_name + "_META" in metadata.tables:
                metadata.tables[table_name + "_META"].drop(self.engine)
                log.info(f"Dropped table {table_name+'_META'}")
            if "TMP_" + table_name in metadata.tables:
                metadata.tables["TMP_" + table_name].drop(self.engine)
                log.info(f"Dropped table {'TMP_'+table_name}")

    def drop_meta_tables(self) -> None:
        """
        Drops metadata tables from the database.
        """
        log.info("Drop Meta tables")
        try:
            # self.drop_table("FITS2DB_TABLE_META")
            # self.drop_table("FITS2DB_META")
            log.info("Finish dropping Meta tables")

        except Exception as err:
            log.error(err)
            raise

    def _fetch_column_details(self, table_name: str) -> Dict[str, Any]:
        """
        Fetches the details of columns in a specified table.

        Args:
            table_name (str): The name of the table to fetch details for.

        Returns:
            Dict[str, Any]: A dictionary mapping column names to their types.
        """
        meta = MetaData()
        table = Table(table_name, meta, autoload_with=self.engine)
        return {column.name: column.type for column in table.columns}

    def _add_missing_columns(
        self,
        source_table_details: Dict[str, Any],
        target_table: str,
        target_table_details: Dict[str, Any],
    ) -> None:
        """
        Adds missing columns to a target table based on the source table's details.

        Args:
            source_table_details (Dict[str, Any]): Details of the source table's columns.
            target_table (str): The name of the target table.
            target_table_details (Dict[str, Any]): Details of the target table's columns.
        """
        with self.engine.connect() as conn:
            for column, col_type in source_table_details.items():
                if column not in target_table_details:
                    alter_query = f"ALTER TABLE {target_table} ADD COLUMN {column} {col_type}"
                    conn.execute(text(alter_query))
                    log.info(
                        f"Added column {column} of type {col_type} to {target_table}"
                    )

    def update_table(self, table_name: str, df: pd.DataFrame) -> None:
        """
        Updates a table in the database by replacing its content with a DataFrame.

        Args:
            table_name (str): The name of the table to update.
            df (pd.DataFrame): The DataFrame containing the data to update.
        """
        log.debug("Passed engine:")
        log.debug(self.engine)
        try:
            tmp_tbl = "TMP_" + table_name
            with self.engine.connect() as conn:
                df.to_sql(
                    name=table_name,
                    con=conn,
                    if_exists="replace",
                    index=False,
                )
                log.info(f"Temporary table {tmp_tbl} created.")

        except Exception as err:
            log.error(err)
            raise

    def upsert_data_table(self, table_name: str, df: pd.DataFrame) -> None:
        """
        Upserts data into a table in the database. If the table exists, merges the data.
        Otherwise, renames the temporary table.

        Args:
            table_name (str): The name of the table to upsert.
            df (pd.DataFrame): The DataFrame containing the data to upsert.
        """
        log.debug("Passed engine:")
        log.debug(self.engine)
        try:
            tmp_tbl = "TMP_" + table_name
            with self.engine.connect() as conn:
                df.to_sql(
                    name=tmp_tbl,
                    con=conn,
                    if_exists="replace",
                    index=False,
                )
                log.info(f"Temporary table {tmp_tbl} created.")

            if self.check_table_exists(table_name):
                self.merge_tables(table_name, tmp_tbl)
                self.drop_table(tmp_tbl)
            else:
                self.rename_table(tmp_tbl, table_name)

        except Exception as err:
            log.error(err)
            raise

    def check_table_exists(self, table_name: str) -> bool:
        """
        Checks if a table exists in the database.

        Args:
            table_name (str): The name of the table to check.

        Returns:
            bool: True if the table exists, False otherwise.
        """
        with self.engine.connect() as conn:
            query = text("SHOW TABLES LIKE :table_name")
            result = conn.execute(query, {"table_name": table_name})
            return result.fetchone() is not None

    def drop_table(self, table_name: str) -> bool:
        """
        Drops a table from the database.

        Args:
            table_name (str): The name of the table to drop.

        Returns:
            bool: True if the table was successfully dropped, False otherwise.
        """
        with self.engine.connect() as conn:
            transaction = conn.begin()  # Start a new transaction
            try:
                # Safely create the SQL string with the table name included
                query = text(f"DROP TABLE `{table_name}`")
                conn.execute(query)
                transaction.commit()  # Commit the transaction if the drop is successful
                return True
            except Exception as e:
                transaction.rollback()  # Roll back the transaction on error
                print(f"Failed to drop table {table_name}: {e}")
                return False

    def rename_table(self, old_name: str, new_name: str) -> None:
        """
        Renames a table in the database and adds an auto-incrementing primary key.

        Args:
            old_name (str): The current name of the table.
            new_name (str): The new name for the table.
        """
        with self.engine.connect() as conn:
            try:
                rename_stmt = text(f"RENAME TABLE {old_name} TO {new_name}")
                id_stmt = text(f"""ALTER TABLE {new_name} 
                                ADD COLUMN id INT AUTO_INCREMENT,
                                ADD PRIMARY KEY (id);""")
                conn.execute(rename_stmt)
                conn.execute(id_stmt)
                log.info(
                    f"Table renamed from {old_name} to {new_name} and added primamry key id."
                )
            except exc.SQLAlchemyError as err:
                log.error(err)
                raise

    def execute_sql(self, sql: str) -> None:
        """
        Executes a raw SQL query against the database.

        Args:
            sql (str): The SQL query to execute.
        """
        with self.engine.connect() as conn:
            try:
                conn.execute(text(sql))
                log.info("Query executed successfully")
            except SQLAlchemyError as e:
                error = str(e.__dict__["orig"])
                log.error(error)

    def merge_tables(self, original_table: str, tmp_table: str) -> None:
        """
        Merges data from a temporary table into the original table.

        Args:
            original_table (str): The name of the original table.
            tmp_table (str): The name of the temporary table.
        """
        source_table_details = self._fetch_column_details(tmp_table)
        target_table_details = self._fetch_column_details(original_table)
        self._add_missing_columns(
            source_table_details, original_table, target_table_details
        )
        with self.engine.connect() as conn:
            transaction = conn.begin()
            try:
                common_columns = ", ".join(
                    set(source_table_details.keys())
                    & set(target_table_details.keys())
                )
                insert_query = f"""
                INSERT INTO {original_table} ({common_columns})
                SELECT {common_columns}
                FROM {tmp_table}
                """
                result = conn.execute(text(insert_query))
                transaction.commit()  # Commit the transaction
                log.info(
                    f"Data inserted successfully, {result.rowcount} rows affected."
                )
            except Exception as e:
                transaction.rollback()  # Rollback the transaction on error
                log.error(f"An error occurred: {e}")

    def close_connection(self) -> None:
        """
        Closes the database connection pool.
        """
        self.engine.dispose()
        log.info("Database connection pool has been closed.")
