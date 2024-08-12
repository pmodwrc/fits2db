"""
Fits2db: A command-line tool to load and manage FITS files in a SQL database.

This tool is designed to be database-agnostic and easily extensible,
leveraging SQLAlchemy for efficient database management.

For detailed documentation, visit: https://pmodwrc.github.io/fits2db/
"""

from .core import Fits2db

__all__ = ["Fits2db"]
