import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

@pytest.fixture(scope='module')
def db_engine():
    engine = create_engine('mysql+mysqlconnector://user:userpassword@localhost/fitsdata')
    yield engine
    engine.dispose()

@pytest.fixture(scope='function')
def db_session(db_engine):
    """Create a session to interact with the test database."""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    yield session

    session.close()
    transaction.rollback()
    connection.close()

def test_merge_data(db_session):
    # Setup test data
    db_session.execute("INSERT INTO table_name (id, data) VALUES (1, 'Initial')")
    db_session.commit()

    # Perform merge (this should be replaced by your actual merge function)
    db_session.execute("REPLACE INTO table_name (id, data) VALUES (1, 'Updated')")
    db_session.commit()

    # Verify results
    result = db_session.execute("SELECT data FROM table_name WHERE id=1")
    assert result.fetchone()[0] == 'Updated'