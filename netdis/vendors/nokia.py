"""
This module connects to a Nokia SROS device using Netmiko library, retrieves information using show commands,
and saves the outputs to a PostgreSQL database.
"""

from typing import List, Tuple

import textfsm
from netmiko import ConnectHandler

# Define the device information
device = {
    'device_type': 'nokia_sros',
    'host': 'clab-vm-sros',
    'username': 'admin',
    'password': 'password',
}

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
    for row in parsed_output:
        chassis_info = dict(zip(headers, row))
        print(chassis_info)


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
    for row in parsed_output:
        card_info = dict(zip(headers, row))
        print(card_info)


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
    for row in parsed_output:
        mda_info = dict(zip(headers, row))
        print(mda_info)


if __name__ == '__main__':
    with ConnectHandler(**device) as net_connect:
        show_chassis_info(net_connect)
        show_card_detail_info(net_connect)
        show_mda_detail_info(net_connect)
