"""
Here are the Metadata table descriptions:

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
This module defines the SQLAlchemy ORM models for the metadata
tables used in the database. The models include:

- Fits2DbMeta: Represents metadata for FITS files.
- Fits2DbTableMeta: Represents metadata for tables related to FITS files.

The relationships between these tables are visualized in the diagram above.
"""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Fits2DbMeta(Base):
    """
    SQLAlchemy ORM model representing the FITS2DB_META table.

    Attributes:
        id (int): Primary key, auto-incremented.
        filename (str): Name of the FITS file.
        filepath (str): Path to the FITS file.
        last_db_update (datetime): Timestamp of the last database update.
        last_file_mutation (datetime): Timestamp of the last file modification.
        tables (relationship): Relationship to the Fits2DbTableMeta objects
                associated with this file.

    """

    __tablename__ = "fits2db_meta"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(Text)
    filepath = Column(Text)
    last_db_update = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
    last_file_mutation = Column(
        DateTime,
        default=datetime.now(timezone.utc),
    )
    # Relationship to associate files with their tables
    tables = relationship(
        "Fits2DbTableMeta",
        back_populates="file_meta",
        cascade="all, delete-orphan",
    )


class Fits2DbTableMeta(Base):
    __tablename__ = "fits2db_table_meta"

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_meta_id = Column(Integer, ForeignKey("fits2db_meta.id"))
    tablename = Column(Text)
    record_count = Column(Integer)
    column_count = Column(Integer)

    file_meta = relationship("Fits2DbMeta", back_populates="tables")
