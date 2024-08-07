from sqlalchemy import text, exc, create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import MetaData, Table
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.exc import SQLAlchemyError
from .base import BaseLoader
from ..config.config_model import ConfigType
from ..fits.fits import FitsFile




import pandas as pd
import logging
from typing import Any, Type, Dict

logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
log = logging.getLogger("fits2db")


class MySQL(BaseLoader):
    def __init__(self, config: ConfigType, file: FitsFile):
        self.config = config
        db_url = self.create_db_url()
        engine = create_engine(db_url)
        super().__init__(db_url, engine, config, file)

    def create_db_url(self) -> str:
        """Creates db connection url

        Returns:
            str: Connection url for mysql
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

    def _add_config_types(self):
        pass


    def drop_tables(self):
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

    def drop_meta_tables(self):
        log.info("Drop Meta tables")
        try:
            #self.drop_table("FITS2DB_TABLE_META")
            #self.drop_table("FITS2DB_META")
            log.info("Finish dropping Meta tables")

        except Exception as err:
            log.error(err)
            raise

    def _fetch_column_details(self, table_name):
        meta = MetaData()
        table = Table(table_name, meta, autoload_with=self.engine)
        return {column.name: column.type for column in table.columns}

    def _add_missing_columns(
        self, source_table_details, target_table, target_table_details
    ):
        with self.engine.connect() as conn:
            for column, col_type in source_table_details.items():
                if column not in target_table_details:
                    alter_query = f"ALTER TABLE {target_table} ADD COLUMN {column} {col_type}"
                    conn.execute(text(alter_query))
                    log.info(
                        f"Added column {column} of type {col_type} to {target_table}"
                    )

    def update_table(self, table_name: str, df: pd.DataFrame) -> None:
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
        with self.engine.connect() as conn:
            query = text("SHOW TABLES LIKE :table_name")
            result = conn.execute(query, {"table_name": table_name})
            return result.fetchone() is not None

    def drop_table(self, table_name: str) -> bool:
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

    def execute_sql(self, sql: str):
        with self.engine.connect() as conn:
            try:
                conn.execute(text(sql))
                log.info("Query executed successfully")
            except SQLAlchemyError as e:
                error = str(e.__dict__["orig"])
                log.error(error)

    def merge_tables(self, original_table: str, tmp_table: str) -> None:
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

    def close_connection(self):
        self.engine.dispose()
        log.info("Database connection pool has been closed.")
