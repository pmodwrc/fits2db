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
from sqlalchemy.orm import Session

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


@pytest.fixture
def update_db_config():
    current_dir = os.path.dirname(__file__)
    sample_config_file = os.path.join(current_dir, "config_update.yml")
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
        self.file_name = f"{self.file_path}.fits"
        self.absolute_path = Path(f"E:/data/{self.file_path}.fits")
        self.file_path = f"E:/data/{self.file_path}.fits"
        self.mtime = time.ctime(time.time())
        self.mdate = datetime.datetime.fromtimestamp(time.time())
        self.tables = {}
        self.corrupt = False
        self.false_ts = False
        return

    def mock_get_table(self, name):
        if self.tables.get(name, None) is not None:
            return self.tables[name]
        data = pd.DataFrame()
        # dti = pd.date_range("2023-06-07 6:00:00", periods=11, freq='15Min 0S')
        if self.false_ts:
            data["timestamp"] = [
                "".join(choice(string.hexdigits) for i in range(12))
                for i in range(11)
            ]
        else:
            dti = pd.date_range("2023-06-07 6:00:00", periods=11, freq="15Min")
            data["timestamp"] = dti
            data["timestamp"] = data["timestamp"].dt.strftime(
                "%Y-%m-%d %H:%M:%S")
            data["stringstamp"] = data["timestamp"]

        if self.corrupt:
            data["Param A"] = list('corrupt_' + string.ascii_lowercase)[:11]
            data["file meta id"] = 'corrupt id'
        else:
            data["PaRaM A"] = list(string.ascii_lowercase)[:11]
            data["PaRaM A a"] = [
                self.prefix + c * 2 for c in list(string.ascii_lowercase)[:11]
            ]
            data["pArAm b"] = [i for i in range(11)]
            data["pARAm C"] = [i / 8 for i in range(11)]
            data["pARAm d"] = [i / 8 * (-1)**i for i in range(11)]
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
        self.tables[name] = table
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
    test_file = fits.FitsFile("file1")
    test_file.prefix = '1_'
    ada = MySQL(db_config, test_file)
    ada.upload_file()
    with db_engine.connect() as conn:
        metadata = MetaData()
        metadata.reflect(bind=conn)
        tables = metadata.sorted_tables
        table_names = [table.name for table in tables]
        tablea = pd.read_sql('SELECT * FROM testtablea', conn)
        tableb = pd.read_sql('SELECT * FROM testtableb', conn)
    # Assert if all the tables were created
    assert set(table_names) == set([
        "fits2db_meta",
        "testtablea",
        "testtablea_meta",
        "testtableb",
        "testtableb_meta",
        "fits2db_table_meta",
    ])

    # Assert correctness of some column
    assert tablea['param_a'].to_list().sort() == test_file.get_table(
        'testtablea').data['PaRaM A'].to_list().sort()
    assert tableb['param_b'].to_list().sort() == test_file.get_table(
        'testtableb').data['pARAm C'].to_list().sort()


# @pytest.mark.parametrize("db_config", [("config_update.yml")], indirect=True)
def test_second_upload(mock_fits_file, db_config, db_engine):
    test_file = fits.FitsFile("file2")
    test_file.prefix = '2_'
    ada = MySQL(db_config, test_file)
    ada.upload_file()
    with db_engine.connect() as conn:
        metadata = MetaData()
        metadata.reflect(bind=conn)
        tables = metadata.sorted_tables
        table_names = [table.name for table in tables]
        file_data = pd.read_sql(
            "SELECT * FROM fits2db_meta WHERE filename like 'file2%'", conn)
        id = file_data['id'][0]
        tablea = pd.read_sql(
            f'SELECT * FROM testtablea WHERE file_meta_id = {id}', conn)
        tableb = pd.read_sql(
            f'SELECT * FROM testtableb WHERE file_meta_id = {id}', conn)
        count = pd.read_sql('SELECT count(timestamp) as a FROM testtablea',
                            conn)
        row_num = count['a'][0]
    # Asseert if the right tables are in the database
    assert set(table_names) == set([
        "fits2db_meta",
        "testtablea",
        "testtablea_meta",
        "testtableb",
        "testtableb_meta",
        "fits2db_table_meta",
    ])
    # assert right ammount of rows
    assert row_num == 22

    # Assert right content of selected columns
    assert tablea['param_a'].to_list().sort() == test_file.get_table(
        'testtablea').data['PaRaM A'].to_list().sort()
    assert tablea['param_a_a'].to_list().sort() == test_file.get_table(
        'testtablea').data['PaRaM A a'].to_list().sort()
    assert tableb['param_b'].to_list().sort() == test_file.get_table(
        'testtableb').data['pARAm C'].to_list().sort()


def test_update(mock_fits_file, update_db_config, db_engine):
    test_file = fits.FitsFile("file1")
    test_file.prefix = '1.1_'
    ada = MySQL(update_db_config, test_file)
    ada.update_file()
    with db_engine.connect() as conn:
        metadata = MetaData()
        metadata.reflect(bind=conn)
        tables = metadata.sorted_tables
        table_names = [table.name for table in tables]
        file_data = pd.read_sql(
            "SELECT * FROM fits2db_meta WHERE filename like 'file1%'", conn)
        id = file_data['id'][0]
        tablea = pd.read_sql(
            f'SELECT * FROM testtablea WHERE file_meta_id = {id}', conn)
        tableb = pd.read_sql(
            f'SELECT * FROM testtableb WHERE file_meta_id = {id}', conn)
        tablec = pd.read_sql(
            f'SELECT * FROM testtableb WHERE file_meta_id = {id}', conn)
        count_a = pd.read_sql('SELECT count(timestamp) as a FROM testtablea',
                              conn)
        count_b = pd.read_sql('SELECT count(timestamp) as a FROM testtableb',
                              conn)
        count_c = pd.read_sql('SELECT count(timestamp) as a FROM testtablec',
                              conn)
        row_num_a = count_a['a'][0]
        row_num_b = count_b['a'][0]
        row_num_c = count_c['a'][0]
    assert set(table_names) == set([
        "fits2db_meta",
        "testtablea",
        "testtablea_meta",
        "testtableb",
        "testtableb_meta",
        "fits2db_table_meta",
        "testtablec",
        "testtablec_meta",
    ])
    # assert that the old contnent of file1 was overwritten
    param_a_a = tablea['param_a_a']
    param_a_a = param_a_a.apply(lambda x: x.startswith('1.1_'))
    assert param_a_a.all()

    # assert that in the table not specified in the config, the data was not updated
    param_a_a = tableb['param_a_a']
    param_a_a = param_a_a.apply(lambda x: x.startswith('1_'))
    assert param_a_a.all()

    # assert correct ammount of rows in each column
    assert row_num_a == 22
    assert row_num_b == 22
    assert row_num_c == 11


def test_remove_row(mock_fits_file, update_db_config, db_engine):
    test_file = fits.FitsFile("file1")
    test_file.prefix = '1.2_'
    update_db_config['fits_files']['delete_rows_from_missing_tables'] = True
    ada = MySQL(update_db_config, test_file)
    ada.update_file()
    with db_engine.connect() as conn:
        metadata = MetaData()
        metadata.reflect(bind=conn)
        tables = metadata.sorted_tables
        table_names = [table.name for table in tables]
        file_data = pd.read_sql(
            "SELECT * FROM fits2db_meta WHERE filename like 'file1%'", conn)
        id = file_data['id'][0]
        tablea = pd.read_sql(
            f'SELECT * FROM testtablea WHERE file_meta_id = {id}', conn)
        tableb = pd.read_sql(
            f'SELECT * FROM testtableb WHERE file_meta_id = {id}', conn)
        tablec = pd.read_sql(
            f'SELECT * FROM testtableb WHERE file_meta_id = {id}', conn)
        count_a = pd.read_sql('SELECT count(timestamp) as a FROM testtablea',
                              conn)
        count_b = pd.read_sql('SELECT count(timestamp) as a FROM testtableb',
                              conn)
        count_c = pd.read_sql('SELECT count(timestamp) as a FROM testtablec',
                              conn)
        row_num_a = count_a['a'][0]
        row_num_b = count_b['a'][0]
        row_num_c = count_c['a'][0]
    assert set(table_names) == set([
        "fits2db_meta",
        "testtablea",
        "testtablea_meta",
        "testtableb",
        "testtableb_meta",
        "fits2db_table_meta",
        "testtablec",
        "testtablec_meta",
    ])
    # Assert corrrect updates of tables
    param_a_a = tablea['param_a_a']
    param_a_a = param_a_a.apply(lambda x: x.startswith('1.2_'))
    assert param_a_a.all()

    param_a_a = tablec['param_a_a']
    param_a_a = param_a_a.apply(lambda x: x.startswith('1.2_'))
    assert param_a_a.all()

    # assert that content of not configured table was removed
    assert len(tableb.index) == 0

    # assert correct row numbers in each table
    assert row_num_a == 22
    assert row_num_b == 11
    assert row_num_c == 11


def test_upload_error(mock_fits_file, update_db_config, db_engine):
    test_file = fits.FitsFile("file3")
    test_file.prefix = '3_'
    test_file.corrupt = True
    ada = MySQL(update_db_config, test_file)
    ada.upload_file()
    with db_engine.connect() as conn:
        metadata = MetaData()
        metadata.reflect(bind=conn)
        tables = metadata.sorted_tables
        table_names = [table.name for table in tables]
        file_data = pd.read_sql(
            "SELECT * FROM fits2db_meta WHERE filename like 'file3%'", conn)
        testtable_a = pd.read_sql('SELECT * FROM testtablea', conn)
        count_a = pd.read_sql('SELECT count(timestamp) as a FROM testtablea',
                              conn)
        count_b = pd.read_sql('SELECT count(timestamp) as a FROM testtableb',
                              conn)
        count_c = pd.read_sql('SELECT count(timestamp) as a FROM testtablec',
                              conn)
        row_num_a = count_a['a'][0]
        row_num_b = count_b['a'][0]
        row_num_c = count_c['a'][0]
    assert set(table_names) == set([
        "fits2db_meta",
        "testtablea",
        "testtablea_meta",
        "testtableb",
        "testtableb_meta",
        "fits2db_table_meta",
        "testtablec",
        "testtablec_meta",
    ])
    # Assert that no content of the file was uploaded, as it had corrupt data
    assert len(file_data.index) == 0

    assert not testtable_a['param_a'].str.startswith('corrupt').any()

    assert row_num_a == 22
    assert row_num_b == 11
    assert row_num_c == 11


def test_update_error(mock_fits_file, update_db_config, db_engine):
    test_file = fits.FitsFile("file1")
    test_file.prefix = '1.4_'
    test_file.corrupt = True
    ada = MySQL(update_db_config, test_file)
    ada.update_file()
    with db_engine.connect() as conn:
        metadata = MetaData()
        metadata.reflect(bind=conn)
        tables = metadata.sorted_tables
        table_names = [table.name for table in tables]
        file_data = pd.read_sql(
            "SELECT * FROM fits2db_meta WHERE filename like 'file3%'", conn)
        testtable_a = pd.read_sql('SELECT * FROM testtablea', conn)
        count_a = pd.read_sql('SELECT count(timestamp) as a FROM testtablea',
                              conn)
        count_b = pd.read_sql('SELECT count(timestamp) as a FROM testtableb',
                              conn)
        count_c = pd.read_sql('SELECT count(timestamp) as a FROM testtablec',
                              conn)
        row_num_a = count_a['a'][0]
        row_num_b = count_b['a'][0]
        row_num_c = count_c['a'][0]
    assert set(table_names) == set([
        "fits2db_meta",
        "testtablea",
        "testtablea_meta",
        "testtableb",
        "testtableb_meta",
        "fits2db_table_meta",
        "testtablec",
        "testtablec_meta",
    ])
    # asserct that the file was not updated
    assert not testtable_a['param_a'].str.startswith('corrupt').any()

    assert row_num_a == 22
    assert row_num_b == 11
    assert row_num_c == 11


def test_bad_timestamp(mock_fits_file, update_db_config, db_engine):
    test_file = fits.FitsFile("file4")
    test_file.prefix = '4_'
    test_file.false_ts = True
    ada = MySQL(update_db_config, test_file)
    ada.upload_file()
    with db_engine.connect() as conn:
        metadata = MetaData()
        metadata.reflect(bind=conn)
        tables = metadata.sorted_tables
        table_names = [table.name for table in tables]
        file_data = pd.read_sql(
            "SELECT * FROM fits2db_meta WHERE filename like 'file3%'", conn)
        testtable_a = pd.read_sql('SELECT * FROM testtablea', conn)
        count_a = pd.read_sql('SELECT count(timestamp) as a FROM testtablea',
                              conn)
        count_b = pd.read_sql('SELECT count(timestamp) as a FROM testtableb',
                              conn)
        count_c = pd.read_sql('SELECT count(timestamp) as a FROM testtablec',
                              conn)
        row_num_a = count_a['a'][0]
        row_num_b = count_b['a'][0]
        row_num_c = count_c['a'][0]
    assert set(table_names) == set([
        "fits2db_meta",
        "testtablea",
        "testtablea_meta",
        "testtableb",
        "testtableb_meta",
        "fits2db_table_meta",
        "testtablec",
        "testtablec_meta",
    ])
    assert len(file_data.index) == 0

    assert not testtable_a['param_a'].str.startswith('corrupt').any()

    assert row_num_a == 22
    assert row_num_b == 11


def test_bad_timestamp_update(mock_fits_file, update_db_config, db_engine):
    test_file = fits.FitsFile("file1")
    test_file.prefix = '1.5_'
    test_file.false_ts = True
    ada = MySQL(update_db_config, test_file)
    ada.upload_file()
    with db_engine.connect() as conn:
        metadata = MetaData()
        metadata.reflect(bind=conn)
        tables = metadata.sorted_tables
        table_names = [table.name for table in tables]
        file_data = pd.read_sql(
            "SELECT * FROM fits2db_meta WHERE filename like 'file1%'", conn)
        id = file_data['id'][0]
        tablea = pd.read_sql(
            f'SELECT * FROM testtablea WHERE file_meta_id = {id}', conn)
        tableb = pd.read_sql(
            f'SELECT * FROM testtableb WHERE file_meta_id = {id}', conn)
        tablec = pd.read_sql(
            f'SELECT * FROM testtableb WHERE file_meta_id = {id}', conn)
        testtable_a = pd.read_sql('SELECT * FROM testtablea', conn)
        count_a = pd.read_sql('SELECT count(timestamp) as a FROM testtablea',
                              conn)
        count_b = pd.read_sql('SELECT count(timestamp) as a FROM testtableb',
                              conn)
        count_c = pd.read_sql('SELECT count(timestamp) as a FROM testtablec',
                              conn)
        row_num_a = count_a['a'][0]
        row_num_b = count_b['a'][0]
        row_num_c = count_c['a'][0]
    assert set(table_names) == set([
        "fits2db_meta",
        "testtablea",
        "testtablea_meta",
        "testtableb",
        "testtableb_meta",
        "fits2db_table_meta",
        "testtablec",
        "testtablec_meta",
    ])
    param_a_a = tablea['param_a_a']
    param_a_a = param_a_a.apply(lambda x: x.startswith('1.2_'))
    assert param_a_a.all()

    param_a_a = tablec['param_a_a']
    param_a_a = param_a_a.apply(lambda x: x.startswith('1.2_'))

    assert param_a_a.all()

    assert not testtable_a['param_a'].str.startswith('corrupt').any()

    assert row_num_a == 22
    assert row_num_b == 11


def test_get_tables(mock_fits_file, update_db_config, db_engine):
    test_file = fits.FitsFile("file1")
    ada = MySQL(update_db_config, test_file)
    with Session(db_engine) as session:
        table_names = ada.get_tables(session)

    assert set(table_names) == set([
        "testtablea",
        "testtableb",
        "testtablec",
    ])
    pass


def test_clean_db(mock_fits_file, update_db_config, db_engine):
    test_file = fits.FitsFile('dsaf')
    ada = MySQL(update_db_config, test_file)
    ada.clean_db()
    with db_engine.connect() as conn:
        metadata = MetaData()
        metadata.reflect(bind=conn)
        tables = metadata.sorted_tables
        table_names = [table.name for table in tables]

    # assert that no tables are left in the database
    assert set(table_names) == set()
