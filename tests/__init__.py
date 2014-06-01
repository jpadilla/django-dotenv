import os
import unittest
from dotenv import parse_dotenv, read_dotenv


DOTENV_DATA = {
    'VAR':                  'VALUE',
    'LEFT_SPACED_VAR':      ' LEFT_SPACE_VALUE',
    'QUOTED_VAR':           'QUOTED_VALUE',
    'DOUBLE_QUOTED_VAR':    'QUOTED_VALUE',
    'QUOTED_TWICE_VAR':     "'QUOTED_TWICE_VALUE'",
    'QUOTED_TWICE_VAR_2':   '"QUOTED_TWICE_VALUE"',
}

class ParseDotenvTests(unittest.TestCase):

    def test_parse_all_variables(self):
        for key, val in DOTENV_DATA.items():
            self.assertIn(key, self.environ.keys())
            self.assertEqual(self.environ[key], val)

    def setUp(self):
        self.environ = dict(parse_dotenv('.env'))


class ReadDotenvTests(ParseDotenvTests):

    def setUp(self):
        self.old_environ = os.environ.copy()
        self.environ = os.environ
        read_dotenv('.env')

    def tearDown(self):
        os.environ = self.old_environ

