import pytest
import os
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.environ.get('DATABASE_URL', 'mysql+mysqlconnector://user:password@localhost/test_db')

Base = declarative_base()

# Define a sample table
class SampleTable(Base):
    __tablename__ = 'sample_table'
    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(String(255), nullable=False)

@pytest.fixture(scope='module')
def db_engine():
    engine = create_engine(DATABASE_URL, echo=True)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()

@pytest.fixture(scope='function')
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()

def test_insert_data(db_session):
    # Insert test data
    new_entry = SampleTable(data='Test Data')
    db_session.add(new_entry)
    db_session.commit()

    # Verify the data was inserted
    result = db_session.query(SampleTable).filter_by(data='Test Data').one()
    assert result.data == 'Test Data'

    # Clean up the test data
    db_session.delete(result)
    db_session.commit()