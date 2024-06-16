"""
This module connects to a Nokia SROS device using Netmiko library, retrieves information using show commands,
and saves the outputs to a PostgreSQL database.
"""

from netmiko import ConnectHandler

from common.vendor_base import VendorBase


class NokiaSros(VendorBase):
    """
    This class represents a Nokia SROS device.

    It provides methods to connect to the device, retrieve information using show commands,
    and save the outputs to a PostgreSQL database.
    """

    def version_info(self, _net_connect):
        """
        Retrieves the version information of the Nokia SROS device.

        Args:
            _net_connect: The Netmiko SSH connection object.

        """
        table_name = 'nokia_version'
        output = _net_connect.send_command('show version')
        template_path = self.discovery_templates_dir + '/nokia_sros_show_version.textfsm'
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
        template_path = self.discovery_templates_dir + '/nokia_sros_show_chassis.textfsm'
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
        template_path = self.discovery_templates_dir + '/nokia_sros_show_card_detail.textfsm'
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
        template_path = self.discovery_templates_dir + '/nokia_sros_show_mda_detail.textfsm'
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
        template_path = self.discovery_templates_dir + '/nokia_sros_show_port_detail.textfsm'
        headers, parsed_output = self.parse_output(output, template_path)
        table_name = 'nokia_transceiver'
        self.recreate_table(table_name, headers)
        self.insert_data_to_table(table_name, headers, parsed_output)

    def service_sdp_info(self, _net_connect):
        """
        Retrieves the service SDP (Service Data Point) information of the Nokia SROS device.

        Args:
            _net_connect: The Netmiko SSH connection object.

        """
        output = _net_connect.send_command('show service sdp')
        template_path = self.discovery_templates_dir + '/nokia_sros_show_service_sdp.textfsm'
        headers, parsed_output = self.parse_output(output, template_path)
        table_name = 'nokia_service_sdp'
        self.recreate_table(table_name, headers)
        self.insert_data_to_table(table_name, headers, parsed_output)

    def service_vpls_info(self, _net_connect):
        """
        Retrieves the service VPLS (Virtual Private LAN Service) information of the Nokia SROS device.

        Args:
            _net_connect: The Netmiko SSH connection object.

        """
        # output = _net_connect.send_command('show service service-using vpls')
        output = """
===============================================================================
Services [vpls]
===============================================================================
ServiceId    Type      Adm  Opr  CustomerId Service Name
-------------------------------------------------------------------------------
110          VPLS      Up   Up   111000     ngn-rtp-zte-msan
201          VPLS      Up   Up   1          vprn-111000|MEDIA-1|TG1_avea_lab
210          VPLS      Up   Up   1          vprn-112000|SIG|TG1
310          VPLS      Down Down 1          Huawei_SBC_Core_Sig
333          VPLS      Up   Up   1          333
373          VPLS      Up   Up   1          373
555          VPLS      Down Down 1          555
801          VPLS      Up   Up   1          vpls-801
1000         VPLS      Up   Up   1          1000
2400         VPLS      Up   Up   1          2400
4091         VPLS      Up   Up   1          zte_dslam_mng
10000        VPLS      Up   Down 1          ELAN001
10001        VPLS      Up   Down 1          ELAN002
10002        VPLS      Up   Down 1          ELAN003
10003        VPLS      Up   Down 1          ELAN004
10004        VPLS      Up   Down 1          ELAN005
16011        VPLS      Down Down 1          16011
17000        b-VPLS    Up   Down 1          17000
18000        b-VPLS    Up   Up   1          18000
20000        b-VPLS    Up   Up   1          20000
22000        b-VPLS    Up   Up   1          22000
25000        b-VPLS    Up   Up   1          25000
55555        VPLS      Up   Up   1          evi-101
69255        VPLS      Up   Up   1          69255
88888        VPLS      Up   Down 1          Time_senk_Uydu_Ku
324749       VPLS      Up   Up   1          324749
324762       VPLS      Up   Up   1          324762
644655       VPLS      Up   Up   1          644655
650865       VPLS      Up   Up   1          650865
652870       VPLS      Up   Up   652870     652870
652871       VPLS      Up   Up   652871     652871
653259       VPLS      Up   Up   1          zyntai|sync
653442       VPLS      Up   Up   1          zyntai|mng
653443       VPLS      Up   Up   1          653443
6969690      VPLS      Up   Up   1          6969690
333333333    VPLS      Up   Up   10         TTiM_to_istAvea|Single_MPLS_Test
-------------------------------------------------------------------------------
Matching Services : 36
-------------------------------------------------------------------------------
===============================================================================
"""
        template_path = self.discovery_templates_dir + '/nokia_sros_show_service_service-using_vpls.textfsm'
        headers, parsed_output = self.parse_output(output, template_path)
        table_name = 'nokia_service_vpls'
        self.recreate_table(table_name, headers)
        self.insert_data_to_table(table_name, headers, parsed_output)

    def service_sap_using_info(self, _net_connect):
        """
        Retrieves the service SAP (Service Access Point) using information of the Nokia SROS device.

        Args:
            _net_connect: The Netmiko SSH connection object.
        """
        output = _net_connect.send_command('show service sap-using')
        template_path = self.discovery_templates_dir + '/nokia_sros_show_service_sap-using.textfsm'
        headers, parsed_output = self.parse_output(output, template_path)
        table_name = 'nokia_service_sap_using'
        self.recreate_table(table_name, headers)
        self.insert_data_to_table(table_name, headers, parsed_output)

    def service_sdp_using_info(self, _net_connect):
        """
        Retrieves the service SDP (Service Data Point) using information of the Nokia SROS device.

        Args:
            _net_connect: The Netmiko SSH connection object.
        """
        output = _net_connect.send_command('show service sdp-using')
        template_path = self.discovery_templates_dir + '/nokia_sros_show_service_sdp-using.textfsm'
        headers, parsed_output = self.parse_output(output, template_path)
        table_name = 'nokia_service_sdp_using'
        self.recreate_table(table_name, headers)
        self.insert_data_to_table(table_name, headers, parsed_output)


if __name__ == '__main__':
    device = NokiaSros('nokia_sros', 'clab-vm-sros', 'admin', 'password')
    # with ConnectHandler(**device.device) as net_connect:
    #     device.version_info(net_connect)
    #     device.chassis_info(net_connect)
    #     device.card_info(net_connect)
    #     device.mda_info(net_connect)
    #     device.transceiver_info(net_connect)
    #     device.service_sdp_info(net_connect)
    #     device.service_sap_using_info(net_connect)
    #     device.service_sdp_using_info(net_connect)
    device.service_vpls_info(None)
