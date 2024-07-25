from ..config.config_model import ConfigType
class DBWriter:
    def load_db(self, config:ConfigType):
        db_type = config["database"]["type"]
        loader = self._get_loader(format)       
        return loader
    
    def _get_loader(self, format:str):
        if format.lower() == 'mysql':
            return 