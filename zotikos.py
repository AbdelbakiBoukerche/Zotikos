import configparser
import zotikos_exceptions
import sys


def main():
    # Get Configuration file
    try:
        get_parser("./conf.ini")
    except zotikos_exceptions.ZotikosConfigFileNotFound as err:
        print(str(err))
        sys.exit(1)
    except zotikos_exceptions.ZotikosException as err:
        print(str(err))
        sys.exit(1)

    print("Hello World!")


def get_parser(path: str):
    config = configparser.ConfigParser()
    try:
        with open(path) as file:
            config.read_file(file)
            return config
    except IOError:
        raise zotikos_exceptions.ZotikosConfigFileNotFound(
            msg="File Not Found. Quitting...")
    except Exception:
        raise zotikos_exceptions.ZotikosException(
            msg="Error while executing the program. Quitting...")


if __name__ == '__main__':
    main()
