from abc import ABC, abstractmethod
from sqlalchemy import create_engine, MetaData
import pandas as pd


class BaseLoader(ABC):
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine)

    @abstractmethod
    def create_table_if_not_exists(self, table_name, df: pd.DataFrame):
        pass

    @abstractmethod
    def upsert_data(self, table_name, df: pd.DataFrame, unique_key):
        pass

