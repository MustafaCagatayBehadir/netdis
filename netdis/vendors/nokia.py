"""
This module connects to a Nokia SROS device using Netmiko library, retrieves information using show commands,
and saves the outputs to a PostgreSQL database.
"""

from netmiko import ConnectHandler

from netdis.vendors.vendor_base import VendorBase


class NokiaSros(VendorBase):
    """
    A class representing a Nokia SROS device.

    Args:
        device_type (str): The type of the device.
        host (str): The hostname or IP address of the device.
        username (str): The username for authentication.
        password (str): The password for authentication.

    Attributes:
        device (dict): A dictionary containing the device information.

    """

    def version_info(self, _net_connect):
        """
        Retrieves the version information of the Nokia SROS device.

        Args:
            _net_connect: The Netmiko SSH connection object.

        """
        table_name = 'nokia_version'
        output = _net_connect.send_command('show version')
        template_path = self.template_path + 'nokia_sros_show_version.textfsm'
        headers, parsed_output = self.parse_output(output, template_path)
        self.recreate_table(table_name, headers)
        self.insert_data_to_table(table_name, headers, parsed_output)

    def chassis_info(self, _net_connect):
        """
        Retrieves the chassis information of the Nokia SROS device.

        Args:
            _net_connect: The Netmiko SSH connection object.

        """
        output = _net_connect.send_command('show chassis')
        template_path = self.template_path + 'nokia_sros_show_chassis.textfsm'
        headers, parsed_output = self.parse_output(output, template_path)
        table_name = 'nokia_chassis'
        self.recreate_table(table_name, headers)
        self.insert_data_to_table(table_name, headers, parsed_output)

    def card_info(self, _net_connect):
        """
        Retrieves the card information of the Nokia SROS device.

        Args:
            _net_connect: The Netmiko SSH connection object.

        """
        output = _net_connect.send_command('show card detail')
        template_path = self.template_path + 'nokia_sros_show_card_detail.textfsm'
        headers, parsed_output = self.parse_output(output, template_path)
        table_name = 'nokia_card'
        self.recreate_table(table_name, headers)
        self.insert_data_to_table(table_name, headers, parsed_output)

    def mda_info(self, _net_connect):
        """
        Retrieves the MDA (Multi-Service Data Application) information of the Nokia SROS device.

        Args:
            _net_connect: The Netmiko SSH connection object.

        """
        output = _net_connect.send_command('show mda detail')
        template_path = self.template_path + 'nokia_sros_show_mda_detail.textfsm'
        headers, parsed_output = self.parse_output(output, template_path)
        table_name = 'nokia_mda'
        self.recreate_table(table_name, headers)
        self.insert_data_to_table(table_name, headers, parsed_output)

    def transceiver_info(self, _net_connect):
        """
        Retrieves the transceiver information of the Nokia SROS device.

        Args:
            _net_connect: The Netmiko SSH connection object.

        """
        output = _net_connect.send_command('show port detail')
        template_path = self.template_path + 'nokia_sros_show_port_detail.textfsm'
        headers, parsed_output = self.parse_output(output, template_path)
        table_name = 'nokia_transceiver'
        self.recreate_table(table_name, headers)
        self.insert_data_to_table(table_name, headers, parsed_output)


if __name__ == '__main__':
    device = NokiaSros('nokia_sros', 'clab-vm-sros', 'admin', 'password')
    with ConnectHandler(**device.device) as net_connect:
        device.version_info(net_connect)
        device.chassis_info(net_connect)
        device.card_info(net_connect)
        device.mda_info(net_connect)
        device.transceiver_info(net_connect)
