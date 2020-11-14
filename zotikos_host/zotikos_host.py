from netmiko import ConnectHandler
from netmiko.ssh_exception import NetmikoAuthenticationException
from netmiko.ssh_exception import NetmikoTimeoutException
from paramiko.ssh_exception import SSHException
import logging
import time
from zotikos_parser import zotikos_parser


class ZotikosHost:

    IP_ADDR = None
    PARSER = None
    CORE_LOGGER = None

    def __init__(self, ip_addr: str, index: int,
                 parser: zotikos_parser.ZotikosParser, usr: str,
                 passwd: str, enabled_passwd: str):
        self.CORE_LOGGER = logging.getLogger('ZotikosCore')
        self.IP_ADDR = ip_addr
        self.PARSER = parser
        self.index = index
        self.is_alive = False
        try:
            self.shell = ConnectHandler(device_type='cisco_ios',
                                        host=ip_addr, username=usr,
                                        password=passwd, secret=enabled_passwd)
            self.shell.enable()
            self.is_alive = True
        except NetmikoAuthenticationException as err:
            self.CORE_LOGGER.error(err)
            self.is_alive = False
        except NetmikoTimeoutException as err:
            self.CORE_LOGGER.error(err)
            self.is_alive = False
        except SSHException as err:
            self.CORE_LOGGER.error(err)
            self.is_alive = False

    def __del__(self):
        if self.is_alive:
            self.shell.disconnect()
        else:
            pass

    def configure_hostname(self):
        cmd = 'hostname ' + self.PARSER.get_hostnames()[self.index]
        try:
            self.shell.send_config_set(cmd, exit_config_mode=False)
        except Exception as err:
            self.CORE_LOGGER.error(err)

    def configure_logon_banner(self):
        cmd = 'banner motd ' + ' % ' + str(self.PARSER.get_logon_banner()) \
            + ' %'
        try:
            self.shell.send_config_set(cmd, exit_config_mode=False)
        except Exception as err:
            self.CORE_LOGGER.error(err)

    def configure_vlans(self):
        time.sleep(0.33)
        for number, name in zip(self.PARSER.get_vlans_number(),
                                self.PARSER.get_vlans_names()):
            create_vlan_cmd = 'vlan ' + str(number)
            name_vlan_cmd = 'name ' + str(name)
            cmd = [create_vlan_cmd, name_vlan_cmd]
            try:
                self.shell.send_config_set(cmd, exit_config_mode=False)
            except Exception as err:
                self.CORE_LOGGER.error(err)
