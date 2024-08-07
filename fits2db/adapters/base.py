from abc import ABC, abstractmethod
import pandas as pd
from sqlalchemy import MetaData, engine
from sqlalchemy.sql import select
from sqlalchemy.orm import Session, sessionmaker
from ..config.config_model import ConfigType
from ..fits.fits import FitsFile
from .meta import Fits2DbMeta, Fits2DbTableMeta, Base

import logging

log = logging.getLogger("fits2db")


class BaseLoader(ABC):
    """A baseclass for writing data in a database

    Attributes:

    """

    def __init__(
        self, db_url: str, engine: engine, config: ConfigType, file: FitsFile
    ):
        self.db_url = db_url
        self.engine = engine
        self.config = config
        self.file = file

    def db_session(self) -> Session:
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        return Session()

    def write_file_meta(self) -> None:
        log.debug(f"Filepath {self.file.absolute_path.as_posix()}")
        self.new_file = Fits2DbMeta(
            filename=self.file.file_name,
            filepath=self.file.absolute_path.as_posix(),
            last_file_mutation=self.file.mdate,
        )
        self.session.add(self.new_file)
        self.session.commit()

    def write_table_meta(self, tbl_name: str, df: pd.DataFrame):
        rows, cols = df.shape
        new_table = Fits2DbTableMeta(
            file_meta_id=self.new_file.id,
            tablename=tbl_name,
            record_count=rows,
            column_count=cols,
        )
        self.session.add(new_table)
        self.session.commit()

    def get_tables(self):
        db_table_names = self.session.execute(
            select(Fits2DbTableMeta.tablename)
        ).fetchall()
        db_table_names = [name[0] for name in db_table_names]
        self.db_table_names = set(db_table_names)

    @abstractmethod
    def drop_tables(self):
        pass

    @abstractmethod
    def drop_meta_tables(self):
        pass

    @abstractmethod
    def upsert_data_table(
        self, table_name: str, df: pd.DataFrame, unique_key
    ) -> None:
        pass

    @abstractmethod
    def update_table(
        self, table_name: str, df: pd.DataFrame, unique_key
    ) -> None:
        pass

    def clean_db(self):
        self.session = self.db_session()
        self.get_tables()
        log.info(f"Tables in DB:{self.db_table_names}")
        self.drop_tables()
        self.drop_meta_tables()

    def upsert_file(self):
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
