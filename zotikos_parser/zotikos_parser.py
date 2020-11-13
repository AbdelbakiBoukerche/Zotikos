import configparser
import zotikos_exceptions


class ZotikosParser:

    __instance__ = None
    __config_file = None

    def __init__(self, config_file: configparser.ConfigParser):
        assert(config_file is not None)
        if ZotikosParser.__instance__ is None:
            ZotikosParser.__instance__ = self
        else:
            raise zotikos_exceptions.ZotikosParserInstanceExists(
                msg="Instance of ZotikosParser already exists")
        self.__config_file = config_file

    @staticmethod
    def get_instance(config_file: configparser.ConfigParser):
        if not ZotikosParser.__instance__:
            ZotikosParser(config_file)
        return ZotikosParser.__instance__

    def __to_arry(self, conf_array: str) -> list:
        return conf_array.replace(' ', '').replace('[', '') \
            .replace(']', '').split(',')

    def get_ipv4_addrs(self) -> list:
        if self.__config_file.has_option('HOST', 'ip_addrs'):
            return self.__to_arry(self.__config_file['HOST']['ip_addrs'])
        else:
            raise zotikos_exceptions.ZotikosParserOptionNotFound(
                msg="No ip_addrs option found at HOST section")
