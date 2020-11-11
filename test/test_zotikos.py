
import unittest
import zotikos
import zotikos_exceptions


class TestZotikos(unittest.TestCase):

    def test_throws_when_file_not_found(self):
        self.assertRaises(
            (zotikos_exceptions.ZotikosConfigFileNotFound,
                zotikos_exceptions.ZotikosException),
            zotikos.get_parser, "missing_file")


if __name__ == '__main__':
    unittest.main()
