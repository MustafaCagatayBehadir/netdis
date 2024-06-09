"""
This module contains the `VendorBase` class which provides functionality for parsing output using TextFSM templates,
recreating database tables, and inserting data into tables.

The module includes the following functions:

- `parse_output`: Parses the output using the TextFSM template.
- `recreate_table`: Recreates a database table by dropping and then creating it.
- `insert_data_to_table`: Inserts the parsed output into the specified table.
"""

from typing import List, Tuple

import textfsm
from sqlalchemy import Column, MetaData, String, Table
from sqlalchemy.dialects.postgresql import insert

from netdis.database import get_db_engine

engine = get_db_engine('postgres', 'postgres', 'bts')
metadata = MetaData()
metadata.bind = engine


class VendorBase:
    """
    Base class for vendor-specific functionality.

    This class provides methods for parsing output using TextFSM templates,
    recreating database tables, and inserting data into tables.

    Attributes:
        None
    """

    def __init__(self, device_type: str, host: str, username: str, password: str) -> None:
        self.template_path = 'netdis/textfsm_templates/'
        self.device = {
            'device_type': device_type,
            'host': host,
            'username': username,
            'password': password,
        }

    def parse_output(self, output: str, template_path: str) -> Tuple[List[str], List[List[str]]]:
        """
        Parses the output using the TextFSM template.

        Args:
            output (str): The output to be parsed.
            template_path (str): The path to the TextFSM template.

        Returns:
            Tuple[List[str], List[List[str]]]: A tuple containing the headers as a list of strings and the parsed output as a list of lists.
        """
        with open(template_path, encoding='utf-8') as template:
            fsm = textfsm.TextFSM(template)
            headers = fsm.header
            parsed_output = fsm.ParseText(output)
        return headers, parsed_output

    def recreate_table(self, table_name: str, headers: List[str]):
        """
        Recreates a database table by dropping and then creating it.

        Args:
            table_name (str): The name of the table to be recreated.
            headers (List[str]): A list of column headers for the table.

        Returns:
            None
        """
        columns = [Column('HOSTNAME', String)] + [Column(header, String) for header in headers]
        table = Table(table_name, metadata, *columns)
        table.drop(bind=engine, checkfirst=True)
        table.create(bind=engine)

    def insert_data_to_table(self, table_name: str, headers: List[str], parsed_output: List[List[str]]):
        """
        Inserts the parsed output into the specified table.

        Args:
            table_name (str): The name of the table to insert the data into.
            headers (List[str]): A list of column headers for the table.
            parsed_output (List[List[str]]): The parsed output to be inserted.

        Returns:
            None
        """
        table = Table(table_name, metadata, autoload_with=engine)
        headers = ['HOSTNAME'] + headers
        with engine.connect() as connection:
            for row in parsed_output:
                row = [self.device.get('host')] + [_.strip() for _ in row]
                data = dict(zip(headers, row))
                stmt = insert(table).values(**data).on_conflict_do_nothing()
                connection.execute(stmt)
            connection.commit()
