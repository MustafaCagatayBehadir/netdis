"""
This module provides functions for working with databases using SQLAlchemy.
"""

import sqlalchemy


def get_db_engine(user: str,
                  password: str,
                  db_name: str,
                  host: str = 'localhost',
                  port: int = 5432) -> 'sqlalchemy.engine.Engine':
    """
    Create and return a SQLAlchemy database engine.

    Args:
        user: The username for the database connection.
        password: The password for the database connection.
        db: The name of the database.
        host: The hostname or IP address of the database server. Defaults to 'localhost'.
        port: The port number of the database server. Defaults to 5432.

    Returns:
        The database engine object.

    """
    url = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'
    engine = sqlalchemy.create_engine(url, pool_pre_ping=True)
    return engine
