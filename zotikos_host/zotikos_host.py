from netmiko import ConnectHandler
from netmiko.ssh_exception import NetmikoAuthenticationException
from netmiko.ssh_exception import NetmikoTimeoutException
from paramiko.ssh_exception import SSHException
import time
import logging
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

        try:
            self.shell = ConnectHandler(device_type='cisco_ios',
                                        host=ip_addr, username=usr,
                                        password=passwd, secret=enabled_passwd)
        except NetmikoAuthenticationException as err:
            self.CORE_LOGGER.error(err)
        except NetmikoTimeoutException as err:
            self.CORE_LOGGER.error(err)
        except SSHException as err:
            self.CORE_LOGGER.error(err)

        self.shell.enable()

    def __del__(self):
        self.shell.disconnect()

    def configure_hostname(self):
        cmd = 'hostname ' + self.PARSER.get_hostnames()[self.index]
        try:
            self.shell.send_config_set(cmd, exit_config_mode=False)
        except Exception as err:
            self.CORE_LOGGER.error(err)
