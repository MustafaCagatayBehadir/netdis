"""
This module connects to a Huawei VRP device using Netmiko library, retrieves information using show commands,
and saves the outputs to a PostgreSQL database.
"""

from netmiko import ConnectHandler

from common.vendor_base import VendorBase


class HuaweiVrp(VendorBase):
    """
    This class represents a Huawei VRP device.

    It provides methods to connect to the device, retrieve information using show commands,
    and save the outputs to a PostgreSQL database.
    """

    def version_info(self, _net_connect):
        """
        Retrieves the version information of the Huawei VRP device.

        Args:
            net_connect (object): The network connection object.

        """
        table_name = 'huawei_version'
        output = _net_connect.send_command('display version')
        template_path = self.discovery_templates_dir + '/huawei_vrp_display_version.textfsm'
        headers, parsed_output = self.parse_output(output, template_path)
        self.recreate_table(table_name, headers)
        self.insert_data_to_table(table_name, headers, parsed_output)

    def card_info(self, _net_connect):
        """
        Retrieves the main slot information of the Huawei VRP device.

        Args:
            net_connect (object): The network connection object.

        """
        table_name = 'huawei_card'
        output = _net_connect.send_command('display elabel brief')
        template_path = self.discovery_templates_dir + '/huawei_vrp_display_elabel_brief_card.textfsm'
        headers, parsed_output = self.parse_output(output, template_path)
        self.recreate_table(table_name, headers)
        self.insert_data_to_table(table_name, headers, parsed_output)

    def mda_info(self, _net_connect):
        """
        Retrieves the daughter card information of the Huawei VRP device.

        Args:
            net_connect (object): The network connection object.

        """
        table_name = 'huawei_mda'
        output = _net_connect.send_command('display elabel brief')
        template_path = self.discovery_templates_dir + '/huawei_vrp_display_elabel_brief_mda.textfsm'
        headers, parsed_output = self.parse_output(output, template_path)
        self.recreate_table(table_name, headers)
        self.insert_data_to_table(table_name, headers, parsed_output)

    def transceiver_info(self, _net_connect):
        """
        Retrieves the transceiver information of the Huawei VRP device.

        Args:
            _net_connect: The Netmiko SSH connection object.

        """
        table_name = 'huawei_transceiver'
        output = _net_connect.send_command('display elabel brief')
        template_path = self.discovery_templates_dir + '/huawei_vrp_display_elabel.textfsm'
        headers, parsed_output = self.parse_output(output, template_path)
        self.recreate_table(table_name, headers)
        self.insert_data_to_table(table_name, headers, parsed_output)

    def mpls_ldp_remote_peer_info(self, _net_connect):
        """
        Retrieves the MPLS LDP (Label Distribution Protocol) remote peer information of the Huawei VRP device.

        Args:
            _net_connect: The Netmiko SSH connection object.

        """
        table_name = 'huawei_mpls_ldp_remote_peer'
        output = _net_connect.send_command('display mpls ldp remote-peer')
        template_path = self.discovery_templates_dir + '/huawei_vrp_display_mpls_ldp_remote-peer.textfsm'
        headers, parsed_output = self.parse_output(output, template_path)
        self.recreate_table(table_name, headers)
        self.insert_data_to_table(table_name, headers, parsed_output)

    def vsi_services_info(self, _net_connect):
        """
        Retrieves the VSI (Virtual Switch Instance) services information of the Huawei VRP device.

        Args:
            _net_connect: The Netmiko SSH connection object.

        """
        table_name = 'huawei_vsi_services'
        output = _net_connect.send_command('display vsi services all')
        template_path = self.discovery_templates_dir + '/huawei_vrp_display_vsi_services_all.textfsm'
        headers, parsed_output = self.parse_output(output, template_path)
        self.recreate_table(table_name, headers)
        self.insert_data_to_table(table_name, headers, parsed_output)

    def vsi_info(self, _net_connect):
        """
        Retrieves the VSI (Virtual Switch Instance) information of the Huawei VRP device.

        Args:
            _net_connect: The Netmiko SSH connection object.

        """
        table_name = 'huawei_vsi'
        output = _net_connect.send_command('display vsi')
        template_path = self.discovery_templates_dir + '/huawei_vrp_display_vsi.textfsm'
        headers, parsed_output = self.parse_output(output, template_path)
        self.recreate_table(table_name, headers)
        self.insert_data_to_table(table_name, headers, parsed_output)

    def vsi_peer_info(self, _net_connect):
        """
        Retrieves the VSI (Virtual Switch Instance) peer information of the Huawei VRP device.

        Args:
            _net_connect: The Netmiko SSH connection object.

        """
        table_name = 'huawei_vsi_peer'
        output = _net_connect.send_command('display vsi peer-info')
        template_path = self.discovery_templates_dir + '/huawei_vrp_display_vsi_peer-info.textfsm'
        headers, parsed_output = self.parse_output(output, template_path)
        self.recreate_table(table_name, headers)
        self.insert_data_to_table(table_name, headers, parsed_output)


if __name__ == '__main__':
    device = HuaweiVrp('huawei_vrp', 'clab-vm-vrp', 'admin', 'password')
    # with ConnectHandler(**device.device) as net_connect:
    #     device.version_info(net_connect)
    #     device.card_info(net_connect)
    #     device.mda_info(net_connect)
    #     device.transceiver_info(net_connect)
    #     device.mpls_ldp_remote_peer_info(net_connect)
    #     device.vsi_services_info(net_connect)
    #     device.vsi_info(net_connect)
    #     device.vsi_peer_info(net_connect)