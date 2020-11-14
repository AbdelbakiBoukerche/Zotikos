import configparser
import sys
import getopt
import getpass
import logging
import time
import zotikos_exceptions
from zotikos_parser import zotikos_parser
from zotikos_host import zotikos_host as ZH


def main(argv):
    CORE_LOGGER = get_core_logger()
    CORE_LOGGER.setLevel(logging.INFO)
    ZOTIKOS_PARSER = None
    config_file_path = None
    username = None

    try:
        opts, args = getopt.getopt(argv, "hc:u:")
    except getopt.GetoptError as err:
        CORE_LOGGER.error(err)
        sys.exit(1)

    for opt, arg in opts:
        if opt in ('-h'):
            print("Show help")
            sys.exit(0)
        elif opt in ('-c'):
            config_file_path = str(arg)
        elif opt in ('-u'):
            username = str(arg)

    if config_file_path is None:
        CORE_LOGGER.error("Configuraiton file not specified, use -h for help")
        sys.exit(0)
    if username is None:
        CORE_LOGGER.error("username not specified, use -h for help")
        sys.exit(0)

    passwd = getpass.getpass(prompt='SSH password: ')
    enabled_passwd = getpass.getpass(prompt="Enabled password: ")

    # Get Configuration file
    try:
        ZOTIKOS_PARSER = zotikos_parser.ZotikosParser.get_instance(
            config_file=get_parser(config_file_path))
    except zotikos_exceptions.ZotikosConfigFileNotFound as err:
        CORE_LOGGER.critical(err.msg)
        sys.exit(1)
    except zotikos_exceptions.ZotikosException as err:
        CORE_LOGGER.critical(err.msg)
        sys.exit(1)

    index = 0
    for ip_addr in ZOTIKOS_PARSER.get_ipv4_addrs():
        host = ZH.ZotikosHost(ip_addr, index, ZOTIKOS_PARSER, username,
                              passwd, enabled_passwd)
        if host.is_alive:
            host.configure_logon_banner()
            host.configure_hostname()
            host.configure_vlans()
        time.sleep(1)
        index += 1


def get_parser(path: str):
    config = configparser.ConfigParser()
    try:
        with open(path) as file:
            config.read_file(file)
            return config
    except IOError:
        raise zotikos_exceptions.ZotikosConfigFileNotFound(
            msg="Configuration File Not Found.")
    except Exception:
        raise zotikos_exceptions.ZotikosException(
            msg="A critical error has occurred while executing the program.")


def get_core_logger():
    logging.basicConfig(
        format='%(asctime)s::%(name)s::%(levelname)s - %(message)s -',
        datefmt='%d-%b-%y-%H:%M:%S')
    return logging.getLogger("ZotikosCore")


if __name__ == '__main__':
    main(sys.argv[1:])
