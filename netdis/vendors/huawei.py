"""
This module connects to a Huawei VRP device using Netmiko library, retrieves information using show commands,
and saves the outputs to a PostgreSQL database.
"""

from netmiko import ConnectHandler

from netdis.vendors.outputs.huawei import outputs
from netdis.vendors.vendor_base import VendorBase


class HuaweiVrp(VendorBase):
    """
    This class represents a Huawei VRP device.

    It provides methods to connect to the device, retrieve information using show commands,
    and save the outputs to a PostgreSQL database.
    """

    def version_info(self, _net_connect=None):
        """
        Retrieves the version information of the Huawei VRP device.

        Args:
            net_connect (object): The network connection object.

        """
        table_name = 'huawei_version'
        # output = _net_connect.send_command('display version')
        output = outputs['display_version']
        template_path = self.template_path + 'huawei_vrp_display_version.textfsm'
        headers, parsed_output = self.parse_output(output, template_path)
        self.recreate_table(table_name, headers)
        self.insert_data_to_table(table_name, headers, parsed_output)

    def card_info(self, _net_connect=None):
        """
        Retrieves the main slot information of the Huawei VRP device.

        Args:
            net_connect (object): The network connection object.

        """
        table_name = 'huawei_card'
        # output = _net_connect.send_command('display elabel brief')
        output = outputs['display_elabel_brief']
        template_path = self.template_path + 'huawei_vrp_display_elabel_brief_card.textfsm'
        headers, parsed_output = self.parse_output(output, template_path)
        self.recreate_table(table_name, headers)
        self.insert_data_to_table(table_name, headers, parsed_output)

    def mda_info(self, _net_connect=None):
        """
        Retrieves the daughter card information of the Huawei VRP device.

        Args:
            net_connect (object): The network connection object.

        """
        table_name = 'huawei_mda'
        # output = _net_connect.send_command('display elabel brief')
        output = outputs['display_elabel_brief']
        template_path = self.template_path + 'huawei_vrp_display_elabel_brief_mda.textfsm'
        headers, parsed_output = self.parse_output(output, template_path)
        self.recreate_table(table_name, headers)
        self.insert_data_to_table(table_name, headers, parsed_output)

    def transceiver_info(self, _net_connect):
        """
        Retrieves the transceiver information of the Huawei VRP device.

        Args:
            _net_connect: The Netmiko SSH connection object.

        """


if __name__ == '__main__':
    device = HuaweiVrp('huawei_vrp', 'clab-vm-vrp', 'admin', 'password')
    # with ConnectHandler(**device.device) as net_connect:
    #     device.display_version(net_connect)
    device.version_info()
    device.card_info()
    device.mda_info()
