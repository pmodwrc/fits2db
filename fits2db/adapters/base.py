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
from typing import Dict, Any

import pandas as pd
from sqlalchemy import engine, MetaData, Table, text, inspect, delete
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql import select
from sqlalchemy.exc import SQLAlchemyError

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

    @abstractmethod
    def create_db_url(self) -> str:
        pass

    def db_session(self) -> Session:
        """
        Creates and returns a new SQLAlchemy session for the database.

        Returns:
            Session: A new SQLAlchemy session object.
        """
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        return Session()

    def write_file_meta(self, session: Session) -> None:
        """
        Writes metadata about the FITS file to the database.
        """
        log.debug(f"Filepath {self.file.absolute_path.as_posix()}")
        self.new_file = Fits2DbMeta(
            filename=self.file.file_name,
            filepath=self.file.absolute_path.as_posix(),
            last_file_mutation=self.file.mdate,
        )
        session.add(self.new_file)
        session.commit()

    def write_table_meta(
        self, tbl_name: str, df: pd.DataFrame, session: Session, file_id: int
    ) -> None:
        """
        Writes metadata about a table in the FITS file to the database.

        Args:
            tbl_name (str): The name of the table.
            df (pd.DataFrame): The DataFrame representing the table data.
        """
        rows, cols = df.shape
        table = session.execute(select(Fits2DbTableMeta).filter_by(file_meta_id=file_id, tablename=tbl_name)).scalar_one_or_none()
        if table is None:
            new_table = Fits2DbTableMeta(
                file_meta_id=file_id,
                tablename=str.lower(tbl_name),
                record_count=rows,
                column_count=cols,
            )
            session.add(new_table)
        else:
            table.record_count = rows
            table.column_count = cols
            table.tablename = str.lower(tbl_name)
        session.commit()

        # with self.engine.connect() as conn:
            # transaction = conn.begin()
            # try:
                # if file_id is not None:
                    # delete_stmt = (
                        # delete(original_table_obj)
                        # .where(original_table_obj.c.file_meta_id == file_id)
                    # )
                    # res = conn.execute(delete_stmt)

    def get_tables(self, session: Session) -> set[str]:
        """
        Retrieves and stores the names of all tables currently in the database.
        """
        db_table_names = session.execute(
            select(Fits2DbTableMeta.tablename)
        ).fetchall()
        db_table_names = [name[0] for name in db_table_names]
        return set(db_table_names)

    def drop_user_tables(self, session: Session) -> None:
        """
        Drops FITS2DB created data tables from the database if they exist.
        """
        metadata = MetaData()
        metadata.reflect(bind=self.engine)
        log.info(metadata.tables)
        try:
            # db_table_names = self.get_tables(session)
            # Bugfix that no tables were found
            db_table_names = set(metadata.tables.keys())
            for table_name in db_table_names:
                if table_name in metadata.tables:
                    metadata.tables[table_name].drop(self.engine)
                    log.info(f"Dropped table {table_name}")
                if table_name + "_META" in metadata.tables:
                    metadata.tables[table_name + "_META"].drop(self.engine)
                    log.info(f"Dropped table {table_name+'_META'}")
                if "TMP_" + table_name in metadata.tables:
                    metadata.tables["TMP_" + table_name].drop(self.engine)
                    log.info(f"Dropped table {'TMP_'+table_name}")

        except SQLAlchemyError as e:
            log.error(f"An error occurred while dropping tables: {e}")
        finally:
            self.engine.dispose()

    def delete_meta_tables(self, session: Session) -> None:
        """
        Drops FITS2DB created data tables from the database if they exist.
        """
        log.debug("Start deletion of Meta tables")
        try:
            session.query(Fits2DbTableMeta).delete()
            log.debug("Run delete stmt for Fits2DbTableMeta")
            session.query(Fits2DbMeta).delete()
            log.debug("Commit changes")
            session.commit()
        except SQLAlchemyError as err:
            log.error(err)

    def clean_db(self) -> None:
        """
        Cleans the database by dropping specific tables and metadata tables.
        """
        with self.db_session() as session:
        # Easyer way to drop tables
            meta = MetaData()
            meta.reflect(bind=self.engine)
            for tbl in reversed(meta.sorted_tables):
                tbl.drop(self.engine)

    def get_fits2db_meta(self) -> pd.DataFrame:
        """
        Retrieves the FITS2DB_META table from the database and returns it as a DataFrame.

        Returns:
            pd.DataFrame: The DataFrame containing the FITS2DB_META table data.
        """
        try:
            df = pd.read_sql_table("fits2db_meta", con=self.engine)
            return df
        except Exception as err:
            log.error(err)
            raise

    def upload_file(self) -> None:
        """
        Upserts the FITS file and its tables into the database.
        """
        with self.db_session() as session:
            self.write_file_meta(session)
            table_configs = self.config["fits_files"]["tables"]
            log.debug("Start upserting data")

            updated_tables = []
            faulty_tables = []
            new_tables = []

            for table in table_configs:
                log.debug(f"Table in configs: {table}")
                table_name = table["name"]
                log.info(table_name)
                log.info(table["ingest_all_columns"])
                try:
                    df = self.file.get_table(table_name)
                    table_name = str.lower(table_name)
                    df.data["FILE_META_ID"] = self.new_file.id
                    df.data.columns = map(str.lower, df.data.columns) # change to lower
                    df.meta.columns = map(str.lower, df.meta.columns) # change to lower
                    date_column = table["date_column"]
                    try:
                        df.data = self._prepare_dataframe(df.data, date_column)
                    except ValueError:
                        faulty_tables.append((table_name, date_column))
                        continue

                    self.upsert_data_table(table_name, df.data)
                    if self.check_table_exists(table_name):
                        source_table_details = self._fetch_column_details('tmp_' + table_name)
                        target_table_details = self._fetch_column_details(table_name)
                        source_table_details = {k.lower(): v for k, v in source_table_details.items()}
                        new_columns = self._add_missing_columns(
                            source_table_details, table_name, target_table_details
                        )

                        updated_tables.append((table_name, df, new_columns))
                    else:
                        new_tables.append((table_name, df))
                    continue

                except KeyError as err:
                    # log.error(f"\n {err}")
                    log.warning(err.args[0])

            if len(faulty_tables) > 0:
                log.error(f'Could not upload File {self.file.file_path}')
                for table_name, date_column in faulty_tables:
                    log.error(
                        f'Error while parsing datetime column {date_column} in table {table_name}'
                    )
                self._delete_columns(updated_tables)
                session.delete(self.new_file)
                session.commit()
                for table, df, new_columns in updated_tables: 
                    self.drop_table('tmp_' + table)
                return
            with self.engine.connect() as conn:
                transaction = conn.begin()
                try: 
                    for table, df, new_columns in updated_tables: 
                        self.merge_tables(table, 'tmp_' + table, conn)
                    transaction.commit()
                except Exception as e:
                    transaction.rollback()  # Rollback the transaction on error
                        # TODO delete file entry and exit function
                    self._delete_columns(updated_tables)
                    log.error(f'Could not Upload {self.file.file_path}')
                    log.error(f"An error occurred: {e}")
                    session.delete(self.new_file)
                    session.commit()
                    for table, df, new_columns in updated_tables: 
                        self.drop_table('tmp_' + table)
                    return
            for table, df, new_columns in updated_tables: 
                self.drop_table('tmp_' + table)
                self.update_table(str.lower(table) + "_meta", df.meta) # change to lower
                self.write_table_meta(
                    table, df.data, session, self.new_file.id
                )
            for table, df in new_tables: 
                self.rename_table('tmp_' + table, table)
                self.update_table(str.lower(table) + "_meta", df.meta) # change to lower
                self.write_table_meta(
                    table, df.data, session, self.new_file.id
                )

        # self.write_file_meta(session)

    def update_fits2db_meta(self, session: Session) -> Fits2DbMeta:
        file_record = (
            session.query(Fits2DbMeta)
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
        # file_record.last_file_mutation = self.file.mdate
        return file_record

    def get_current_file_tables(self, session: Session, file_record: Fits2DbMeta):
        tables_to_delete = session.query(Fits2DbTableMeta).filter(
            Fits2DbTableMeta.file_meta_id == file_record.id
        )
        tables = {}
        for table_meta in tables_to_delete:
            tablename = table_meta.tablename
            metadata = MetaData()
            table = Table(tablename, metadata, autoload_with=self.engine)
            tables[tablename] = table
        return tables

    def delete_file_from_table(self, session: Session, file_record: Fits2DbMeta, table: Table):
        tables_to_delete = session.query(Fits2DbTableMeta).filter(
            Fits2DbTableMeta.file_meta_id == file_record.id, Fits2DbTableMeta.tablename == table.name
        )
        tables = {}
        delete_stmt = table.delete().where(
            table.c.file_meta_id == file_record.id # change to lowercase
        )
        session.execute(delete_stmt)
        log.info(
            f"Deleted rows in table '{table.name}' where file_meta_id = {file_record.id}"
        )
        tables_to_delete.delete(synchronize_session=False)
        return tables
    

    def update_fits2db_table(self, session: Session, file_record: Fits2DbMeta):
        """ Delete entries from each table, that belong to a specific file

        Args:
            session (Session): _description_
            file_record (Fits2DbMeta): file meta data from the file whose data is to be deleted
        """
        tables_to_delete = session.query(Fits2DbTableMeta).filter(
            Fits2DbTableMeta.file_meta_id == file_record.id
        )
        for table_meta in tables_to_delete:
            tablename = table_meta.tablename
            metadata = MetaData()
            table = Table(tablename, metadata, autoload_with=self.engine)
            delete_stmt = table.delete().where(
                table.c.file_meta_id == file_record.id # change to lowercase
            )
            session.execute(delete_stmt)
            log.info(
                f"Deleted rows in table '{tablename}' where file_meta_id = {file_record.id}"
            )

        tables_to_delete.delete(synchronize_session=False)

    def update_file(self) -> None:
        """
        Updates the metadata and data of the FITS file in the database.
        """
        with self.db_session() as session:
            file_record = self.update_fits2db_meta(session)
            remaining_tables = self.get_current_file_tables(session, file_record)
            # self.update_fits2db_table(session, file_record)
            session.commit()
            table_configs = self.config["fits_files"]["tables"]
            log.debug("Start upserting data")
            updated_tables = []
            faulty_tables = []
            new_tables = []
            for table in table_configs:
                log.debug(f"Table in configs: {table}")
                table_name = table["name"]
                log.info(table_name)
                log.info(table["ingest_all_columns"])
                try:
                    df = self.file.get_table(table_name)
                    table_name = str.lower(table_name)
                    df.data["FILE_META_ID"] = file_record.id
                    df.data.columns = map(str.lower, df.data.columns)
                    df.meta.columns = map(str.lower, df.meta.columns)
                    date_column = table["date_column"]
                    try:
                        df.data = self._prepare_dataframe(df.data, date_column)
                    except ValueError as err:
                        faulty_tables.append((table_name, date_column))
                        continue

                    self.upsert_data_table(table_name, df.data, file_record.id)
                    remaining_tables.pop(table_name, None)
                    if self.check_table_exists(table_name):
                        source_table_details = self._fetch_column_details('tmp_' + table_name)
                        target_table_details = self._fetch_column_details(table_name)
                        source_table_details = {k.lower(): v for k, v in source_table_details.items()}
                        new_columns = self._add_missing_columns(
                            source_table_details, table_name, target_table_details
                        )

                        updated_tables.append((table_name, df, file_record.id, new_columns))
                    else:
                        new_tables.append((table_name, df, file_record.id))
                    continue

                except KeyError as err:
                    # log.error(f"\n {err}")
                    log.warning(err.args[0])
                
            if len(faulty_tables) > 0:
                log.error(f'Could not update File {self.file.file_path}')
                for table_name, date_column in faulty_tables:
                    log.error(
                        f'Error while parsing datetime column {date_column} in table {table_name}'
                    )
                self._delete_columns(updated_tables)
                session.commit()
                for table, df, file_id, _ in updated_tables: 
                    self.drop_table('tmp_' + table)
                return

            with self.engine.connect() as conn:
                transaction = conn.begin()
                try: 
                    for table, df, file_id, new_columns in updated_tables: 
                        self.merge_tables(table, 'tmp_' + table, conn, file_id)
                    transaction.commit()
                except Exception as e:
                    transaction.rollback()  # Rollback the transaction on error
                    self._delete_columns(updated_tables)
                    # TODO whatabout da file meta STUFF
                    log.error(f"An error occurred: {e}")
                    for table, df, file_id, _ in updated_tables: 
                        self.drop_table('tmp_' + table)
                    return
            for table, df, file_id, _ in updated_tables: 
                self.drop_table('tmp_' + table)
                self.write_table_meta(
                    table, df.data, session, file_record.id
                )
                self.update_table(table + "_META", df.meta)
            for table, df, file_id in new_tables: 
                self.rename_table('tmp_' + table, table)
                self.write_table_meta(
                    table, df.data, session, file_record.id
                )
                self.update_table(table + "_META", df.meta)
            
            if self.config['fits_files']['delete_rows_from_missing_tables']:
                for k, table in remaining_tables.items():
                    self.delete_file_from_table(session, file_record, table)

            file_record.last_file_mutation = self.file.mdate
            session.commit()

    def upsert_data_table(self, table_name: str, df: pd.DataFrame, file_id: int=None) -> None:
        """
        Upserts data into a table in the database. If the table exists, merges the data.
        Otherwise, renames the temporary table.

        Args:
            table_name (str): The name of the table to upsert.
            df (pd.DataFrame): The DataFrame containing the data to upsert.
        """
        log.debug("Passed engine:")
        log.debug(self.engine)

        log.debug('clean df')  # TODO Extract
        

        try:
            tmp_tbl = "tmp_" + str.lower(table_name)  # change to lowercase
            with self.engine.connect() as conn:
                df.to_sql(
                    name=tmp_tbl,
                    con=conn,
                    if_exists="replace",
                    index=False,
                )
                log.info(f"Temporary table {tmp_tbl} created.")

            # if self.check_table_exists(table_name):
                # self.merge_tables(table_name, tmp_tbl, file_id)
                # self.drop_table(tmp_tbl)
            # else:
                # self.rename_table(tmp_tbl, table_name)

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
            except SQLAlchemyError as err:
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

    def merge_tables(self, original_table: str, tmp_table: str, conn, file_id: int=None) -> None:
        """
        Merges data from a temporary table into the original table.

        Args:
            original_table (str): The name of the original table.
            tmp_table (str): The name of the temporary table.
        """
        metadata_obj = MetaData()
        metadata_obj.reflect(bind=self.engine)
        original_table_obj = metadata_obj.tables[str.lower(original_table)]
        tmp_table_obj = metadata_obj.tables[str.lower(tmp_table)]
        source_table_details = self._fetch_column_details(tmp_table)
        target_table_details = self._fetch_column_details(original_table)
        source_table_details = {k.lower(): v for k, v in source_table_details.items()}

        if file_id is not None:
            delete_stmt = (
                delete(original_table_obj)
                .where(original_table_obj.c.file_meta_id == file_id)
            )
            res = conn.execute(delete_stmt)
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

        log.info(
            f"Data inserted successfully, {result.rowcount} rows affected."
        )

    def close_connection(self) -> None:
        """
        Closes the database connection pool.
        """
        self.engine.dispose()
        log.info("Database connection pool has been closed.")

    def _fetch_column_details(self, table_name: str) -> Dict[str, Any]:
        """
        Fetches the details of columns in a specified table.

        Args:
            table_name (str): The name of the table to fetch details for.

        Returns:
            Dict[str, Any]: A dictionary mapping column names to their types.
        """
        meta = MetaData()
        table = Table(str.lower(table_name), meta, autoload_with=self.engine)
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
        added_columns = []
        source_table_details = {k.lower(): v for k, v in source_table_details.items()}
        target_table = str.lower(target_table)
        with self.engine.connect() as conn:
            for column, col_type in source_table_details.items():
                if column not in target_table_details:
                    alter_query = f"ALTER TABLE {target_table} ADD COLUMN {column} {col_type}"
                    conn.execute(text(alter_query))
                    log.info(
                        f"Added column {column} of type {col_type} to {target_table}"
                    )
                    added_columns.append(column)
        return added_columns

    def _delete_columns(self, table_infos):
        with self.engine.connect() as conn:
            for table_info in table_infos:
                table = table_info[0]
                columns = table_info[-1]
                for column in columns:
                    alter_query = f"ALTER TABLE {table} DROP COLUMN {column}"
                    try:
                        conn.execute(text(alter_query))
                        log.info(f"Deleted column {column} in table {table}")
                    # except Exception as e:
                    except SQLAlchemyError as e:
                        log.error(f"Error while deleting {column} from table {table}")
                        # print(type(e))

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
            tmp_tbl = "tmp_" + str.lower(table_name)
            with self.engine.connect() as conn:
                df.to_sql(
                    name=str.lower(table_name),
                    con=conn,
                    if_exists="replace",
                    index=False,
                )
                log.info(f"Temporary table {tmp_tbl} created.")

        except Exception as err:
            log.error(err)
            raise
    
    def _prepare_dataframe(self, data, data_column):
        mapping = {col: ''.join(c for c in col if c.isalnum() or c == ' ' or c == '_') for col in data.columns}
        data = data.rename(columns=mapping)

        space_cols = [col for col in data.columns if ' ' in col]
        mapping = {col: col.replace(' ', '_') for col in space_cols}
        data = data.rename(columns=mapping)

        cols=pd.Series(data.columns)

        for dup in cols[cols.duplicated()].unique(): 
            cols[cols[cols == dup].index.values.tolist()] = [dup + '_' + str(i) if i != 0 else dup for i in range(sum(cols == dup))]

        # rename the columns with the cols list.
        data.columns=cols
        if data_column is not None:
            if data_column in data.columns:
                # data = data.rename(columns={data_column: 'timestamp'})
                data[data_column] = pd.to_datetime(data[data_column]) # FIX TIMESTAMP setting
                data.dropna(subset=[data_column], inplace=True)
                data['timestamp'] = data[data_column] # FIX TIMESTAMP setting
        return data
