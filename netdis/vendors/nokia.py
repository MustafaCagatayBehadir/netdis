"""
This module connects to a Nokia SROS device using Netmiko library, retrieves information using show commands,
and saves the outputs to a PostgreSQL database.
"""

from typing import List, Tuple

import textfsm
from database import get_db_engine
from netmiko import ConnectHandler
from sqlalchemy import Column, MetaData, String, Table, inspect
from sqlalchemy.dialects.postgresql import insert

# Define the device information
device = {
    'device_type': 'nokia_sros',
    'host': 'clab-vm-sros',
    'username': 'admin',
    'password': 'password',
}

engine = get_db_engine('postgres', 'postgres', 'bts')
metadata = MetaData()
metadata.bind = engine

TEMPLATE = 'netdis/textfsm_templates/'


def parse_output(output: str, template_path: str) -> Tuple[List[str], List[List[str]]]:
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


def recreate_table(table_name: str, headers: List[str]):
    """
    Recreates a database table by dropping and then creating it.

    Args:
        table_name (str): The name of the table to be recreated.
        headers (List[str]): A list of column headers for the table.

    Returns:
        None
    """
    columns = [Column(header, String) for header in headers]
    table = Table(table_name, metadata, *columns)
    table.drop(bind=engine, checkfirst=True)
    table.create(bind=engine)


def insert_data_to_table(table_name: str, headers: List[str], parsed_output: List[List[str]]):
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
    with engine.connect() as connection:
        for row in parsed_output:
            data = dict(zip(headers, row))
            stmt = insert(table).values(**data).on_conflict_do_nothing()
            connection.execute(stmt)
        connection.commit()


def show_version(_net_connect):
    """
     Retrieves and returns the version information from a Nokia device.

     Args:
          net_connect (object): The network connection object.

     Returns:
          str: The output of the 'show version' command.

     Raises:
          None

     """
    table_name = 'nokia_version'
    output = _net_connect.send_command('show version')
    template_path = TEMPLATE + 'nokia_sros_show_version.textfsm'
    headers, parsed_output = parse_output(output, template_path)
    recreate_table(table_name, headers)
    insert_data_to_table(table_name, headers, parsed_output)


def show_chassis_info(_net_connect):
    """
    Retrieves and returns the chassis information from a Nokia device.

    Args:
        net_connect (object): The network connection object.

    Returns:
        str: The output of the 'show chassis' command.

    Raises:
        None

    """
    output = _net_connect.send_command('show chassis')
    template_path = TEMPLATE + 'nokia_sros_show_chassis.textfsm'
    headers, parsed_output = parse_output(output, template_path)
    table_name = 'nokia_chassis'
    recreate_table(table_name, headers)
    insert_data_to_table(table_name, headers, parsed_output)


def show_card_detail_info(_net_connect):
    """
    Retrieves and returns the card detail information from a Nokia device.

    Args:
        net_connect (object): The network connection object.

    Returns:
        str: The output of the 'show card detail' command.

    Raises:
        None

    """
    output = _net_connect.send_command('show card detail')
    template_path = TEMPLATE + 'nokia_sros_show_card_detail.textfsm'
    headers, parsed_output = parse_output(output, template_path)
    table_name = 'nokia_card_detail'
    recreate_table(table_name, headers)
    insert_data_to_table(table_name, headers, parsed_output)


def show_mda_detail_info(_net_connect):
    """
    Retrieves and returns the mda detail information from a Nokia device.

    Args:
        net_connect (object): The network connection object.

    Returns:
        str: The output of the 'show mda detail' command.

    Raises:
        None

    """
    output = _net_connect.send_command('show mda detail')
    template_path = TEMPLATE + 'nokia_sros_show_mda_detail.textfsm'
    headers, parsed_output = parse_output(output, template_path)
    table_name = 'nokia_mda_detail'
    recreate_table(table_name, headers)
    insert_data_to_table(table_name, headers, parsed_output)


def show_port_detail(_net_connect):
    """
    Retrieves and returns the port detail information from a Nokia device.

    Args:
        net_connect (object): The network connection object.

    Returns:
        str: The output of the 'show port detail' command.

    Raises:
        None

    """
    output = _net_connect.send_command('show port detail')
    template_path = TEMPLATE + 'nokia_sros_show_port_detail.textfsm'
    headers, parsed_output = parse_output(output, template_path)
    table_name = 'nokia_port_detail'
    recreate_table(table_name, headers)
    insert_data_to_table(table_name, headers, parsed_output)


if __name__ == '__main__':
    with ConnectHandler(**device) as net_connect:
        show_version(net_connect)
        show_chassis_info(net_connect)
        show_card_detail_info(net_connect)
        show_mda_detail_info(net_connect)
        show_port_detail(net_connect)
