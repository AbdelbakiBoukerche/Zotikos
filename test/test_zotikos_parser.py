import unittest
from zotikos_parser import zotikos_parser as zp
import zotikos
import zotikos_exceptions as ze


class TestZotikosParser(unittest.TestCase):
    def setUp(self):
        self.valid_config = zotikos.get_parser('./test/test_conf.ini')

    def test_throws_when_config_file_is_none(self):
        self.assertRaises(AssertionError, zp.ZotikosParser, None)

    def test_throws_when_option_not_found(self):
        parser = zp.ZotikosParser(self.valid_config)
        self.assertRaises(ze.ZotikosParserOptionNotFound,
                          parser.get_ipv4_addrs)

        self.assertRaises(ze.ZotikosParserOptionNotFound,
                          parser.get_hostnames)

        self.assertRaises(ze.ZotikosParserOptionNotFound,
                          parser.get_logon_banner)

        self.assertRaises(ze.ZotikosParserOptionNotFound,
                          parser.get_vlans_number)

        self.assertRaises(ze.ZotikosParserOptionNotFound,
                          parser.get_vlans_names)


if __name__ == '__main__':
    unittest.main()
