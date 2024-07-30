from abc import ABC, abstractmethod
from sqlalchemy import create_engine, MetaData
import pandas as pd
from ..config.config_model import ConfigType
from ..fits.fits import FitsFile

class BaseLoader(ABC):
    """A baseclass for writing data in a database

    Attributes:
        
    """
    def __init__(self, db_url:str, config:ConfigType, file:FitsFile):
        self.engine = create_engine(db_url)
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine)
        self.config = config


    @abstractmethod
    def upsert_table(self, table_name:str, df: pd.DataFrame, unique_key)->None:
        pass

    def upsert_data(self):
        table_configs = self.config["fits_files"]["tables"]
        print("Start upserting data")
        self.upsert_table()



