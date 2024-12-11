import datetime
import os
from pathlib import Path
import time
from fits2db.fits import fits
from fits2db.adapters import MySQL
import fits2db.config as config
import pandas as pd
import pytest
import string
from random import seed
from random import choice
from random import randint
from sqlalchemy import create_engine
from sqlalchemy import MetaData

seed(42)


class FitsTableMockResponse:
    def __init__(self, name, meta, data, create_at, index):
        name = ""
        pass


@pytest.fixture
def db_config():
    current_dir = os.path.dirname(__file__)
    sample_config_file = os.path.join(current_dir, "config.yml")
    configs = config.get_configs(sample_config_file)
    return configs


@pytest.fixture(scope="function")
def db_engine(db_config):
    user = db_config["database"]["user"]
    password = db_config["database"]["password"]
    host = db_config["database"]["host"]
    port = db_config["database"]["port"]
    db_name = db_config["database"]["db_name"]
    url = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db_name}"
    engine = create_engine(url)
    yield engine
    engine.dispose()


@pytest.fixture
def mock_fits_file(monkeypatch):
    def mock_load_file(self):
        self.hdul = 1
        return

    def mock_check_path(self):
        return True

    def mock_post_init(self):
        self.file_path = "E:/data/test.fits"
        self.file_name = "test.fits"
        self.absolute_path = Path("E:/data/test.fits")
        self.mtime = time.ctime(time.time())
        self.mdate = datetime.datetime.fromtimestamp(time.time())
        return

    def mock_get_table(self, name):
        data = pd.DataFrame()
        # dti = pd.date_range("2023-06-07 6:00:00", periods=11, freq='15Min 0S')
        dti = pd.date_range("2023-06-07 6:00:00", periods=11, freq="15Min")
        data["timestamp"] = dti
        data["PaRaM A"] = list(string.ascii_lowercase)[:11]
        data["PaRaM A a"] = [c * 2 for c in list(string.ascii_lowercase)[:11]]
        data["pArAm b"] = [i for i in range(11)]
        data["pARAm C"] = [i / 8 for i in range(11)]
        data["pARAm d"] = [i / 8 * (-1) ** i for i in range(11)]
        data["timestamp"] = data["timestamp"].dt.strftime(
            "%Y-%m-%d %hh:%mm:%ss"
        )
        data["stringstamp"] = data["timestamp"]
        print(data)

        meta = pd.DataFrame()
        meta["keyword"] = [
            "".join(choice(string.hexdigits) for i in range(12))
            for i in range(13)
        ]
        meta["value"] = [
            "".join(choice(string.hexdigits) for i in range(randint(1, 7)))
            for i in range(13)
        ]
        print(meta)
        table = fits.FitsTable(name, meta, data)
        return table

    monkeypatch.setattr(fits.FitsFile, "__post_init__", mock_post_init)
    monkeypatch.setattr(fits.FitsFile, "get_table", mock_get_table)


@pytest.fixture(scope="function")
def clear_database(db_engine):
    with db_engine.connect() as conn:
        metadata = MetaData()
        metadata.reflect(bind=conn)
        metadata.drop_all(bind=conn)
    return True

def test_upload(mock_fits_file, db_config, db_engine, clear_database):
    # if clear_database:
    filet = fits.FitsFile("abs")
    ada = MySQL(db_config, filet)
    ada.upload_file()
    with db_engine.connect() as conn:
        metadata = MetaData()
        metadata.reflect(bind=conn)
        tables = metadata.sorted_tables
        table_names = [table.name for table in tables]
    assert set(table_names) == set([
        "fits2db_meta",
        "testtablea",
        "testtablea_meta",
        "testtableb",
        "testtableb_meta",
        "fits2db_table_meta",
    ])
    # assert filet.get_table('petr') == 'petr'
