import configparser
import sys
import logging
import time
import zotikos_exceptions
from zotikos_parser import zotikos_parser
from zotikos_host import zotikos_host as ZH


def main():
    CORE_LOGGER = get_core_logger()
    CORE_LOGGER.setLevel(logging.INFO)
    ZOTIKOS_PARSER = None

    # Get Configuration file
    try:
        ZOTIKOS_PARSER = zotikos_parser.ZotikosParser.get_instance(
            config_file=get_parser("./conf.ini"))
    except zotikos_exceptions.ZotikosConfigFileNotFound as err:
        CORE_LOGGER.critical(err.msg)
        sys.exit(1)
    except zotikos_exceptions.ZotikosException as err:
        CORE_LOGGER.critical(err.msg)
        sys.exit(1)

    username = "abdelbaki"
    passwd = "passwd"
    enabled_passwd = "cisco"

    index = 0
    for ip_addr in ZOTIKOS_PARSER.get_ipv4_addrs():
        host = ZH.ZotikosHost(ip_addr, index, ZOTIKOS_PARSER, username,
                              passwd, enabled_passwd)
        host.configure_hostname()
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
    main()
