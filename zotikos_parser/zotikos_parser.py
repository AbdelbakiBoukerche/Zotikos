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

    def __to_array(self, conf_array: str) -> list:
        return conf_array.replace(' ', '').replace('[', '') \
            .replace(']', '').split(',')

    def get_ipv4_addrs(self) -> list:
        if self.__config_file.has_option('HOST', 'ip_addrs'):
            return self.__to_array(self.__config_file['HOST']['ip_addrs'])
        else:
            raise zotikos_exceptions.ZotikosParserOptionNotFound(
                msg="No ip_addrs option found in the HOST section")

    def get_hostnames(self) -> list:
        if self.__config_file.has_option('GENERAL', 'hostname'):
            return self.__to_array(self.__config_file['GENERAL']['hostname'])
        else:
            raise zotikos_exceptions.ZotikosParserOptionNotFound(
                msg="No hostname option found in the GENERAL section")

    def get_logon_banner(self) -> list:
        if self.__config_file.has_option('GENERAL', 'banner'):
            return self.__config_file['GENERAL']['banner']
        else:
            raise zotikos_exceptions.ZotikosParserOptionNotFound(
                msg="No banner option found in the GENERAL section")

    def get_vlans_number(self) -> list:
        if self.__config_file.has_option('VLANS', 'vlans_num'):
            vlans_list = self.__to_array(
                self.__config_file['VLANS']['vlans_num'])
            for i in range(0, len(vlans_list)):
                vlans_list[i] = int(vlans_list[i])
            return vlans_list
        else:
            raise zotikos_exceptions.ZotikosParserOptionNotFound(
                msg="No vlans_num option found in the VLANS section")

    def get_vlans_names(self) -> list:
        if self.__config_file.has_option('VLANS', 'vlans_name'):
            return self.__to_array(self.__config_file['VLANS']['vlans_name'])
        else:
            raise zotikos_exceptions.ZotikosParserOptionNotFound(
                msg="No vlans_name option found in the VLANS section")
