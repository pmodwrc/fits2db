from .base import BaseLoader
from ..config.config_model import ConfigType
from ..fits.fits import FitsFile

class MySQL(BaseLoader):
    def __init__(self, config:ConfigType, file:FitsFile):
        self.config = config
        db_url = self.create_db_url()
        super().__init__(db_url, config, file)

    def create_db_url(self):
        user = self.config["database"]["user"]
        password = self.config["database"]["password"]
        host = self.config["database"]["host"]
        port = self.config["database"]["port"]
        db_name = self.config["database"]["db_name"]
        return f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db_name}'

    
    def upsert_table(self):
        print("MySQL upsert")
        #return super().upsert_data(table_name, df, unique_key)
    



