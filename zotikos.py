import configparser
import sys
import logging
import zotikos_exceptions


def main():
    CORE_LOGGER = get_core_logger()
    CORE_LOGGER.setLevel(logging.INFO)
    # Get Configuration file
    try:
        get_parser("./conf.ini")
    except zotikos_exceptions.ZotikosConfigFileNotFound as err:
        CORE_LOGGER.critical(err.msg)
        sys.exit(1)
    except zotikos_exceptions.ZotikosException as err:
        CORE_LOGGER.critical(err.msg)
        sys.exit(1)


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
