"""This file manges the table structure and upload structure to upload data 


```mermaid
erDiagram
    FITS2DB_META {
        int id PK
        varchar filename
        varchar file_path 
        datetime file_last_mutated
    }
    
    FITS2DB_TABLE_META {
        int id PK
        varchar description
        varchar tablename
        int row_cnt
        int col_cnt
    }

    YOUR_TABLE {
        int id PK
        varchar your_data
        int metadata_id FK
    }

    YOUR_TABLE_META {
        int id PK
        text keyword
        text value     
        int metadata_id FK  
    }
    
    FITS2DB_META ||--|| FITS2DB_TABLE_META : "foreign_id"
    FITS2DB_META ||--o| YOUR_TABLE : "foreign_id"
    FITS2DB_TABLE_META ||--o| YOUR_TABLE_META : "metadata_id"
```
"""

from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone


Base = declarative_base()


class Fits2DbMeta(Base):
    __tablename__ = "FITS2DB_META"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(Text)
    filepath = Column(Text)
    last_db_update = Column(DateTime, 
                            default=datetime.now(timezone.utc),
                            onupdate=datetime.now(timezone.utc),)
    last_file_mutation = Column(
        DateTime,
        default=datetime.now(timezone.utc),
    )

    # Relationship to associate files with their tables
    tables = relationship("Fits2DbTableMeta", back_populates="file_meta")


class Fits2DbTableMeta(Base):
    __tablename__ = "FITS2DB_TABLE_META"

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_meta_id = Column(Integer, ForeignKey("FITS2DB_META.id"))
    tablename = Column(Text)
    record_count = Column(Integer)
    column_count = Column(Integer)

    # Relationship to reference the file metadata
    file_meta = relationship("Fits2DbMeta", back_populates="tables")