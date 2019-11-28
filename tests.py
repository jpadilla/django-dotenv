import os
import shutil
import unittest
import warnings

from dotenv import (
    parse_dotenv,
    read_dotenv,
    _read_dotenv_example,
    _check_safe
)

class ParseDotenvTestCase(unittest.TestCase):
    def test_parses_unquoted_values(self):
        env = parse_dotenv('FOO=bar')
        self.assertEqual(env, {'FOO': 'bar'})

    def test_parses_values_with_spaces_around_equal_sign(self):
        env = parse_dotenv('FOO =bar')
        self.assertEqual(env, {'FOO': 'bar'})

        env = parse_dotenv('FOO= bar')
        self.assertEqual(env, {'FOO': 'bar'})

    def test_parses_double_quoted_values(self):
        env = parse_dotenv('FOO="bar"')
        self.assertEqual(env, {'FOO': 'bar'})

    def test_parses_single_quoted_values(self):
        env = parse_dotenv("FOO='bar'")
        self.assertEqual(env, {'FOO': 'bar'})

    def test_parses_escaped_double_quotes(self):
        env = parse_dotenv('FOO="escaped\\"bar"')
        self.assertEqual(env, {'FOO': 'escaped"bar'})

    def test_parses_empty_values(self):
        env = parse_dotenv('FOO=')
        self.assertEqual(env, {'FOO': ''})

    def test_expands_variables_found_in_values(self):
        env = parse_dotenv("FOO=test\nBAR=$FOO")
        self.assertEqual(env, {'FOO': 'test', 'BAR': 'test'})

    def test_expands_variables_wrapped_in_brackets(self):
        env = parse_dotenv("FOO=test\nBAR=${FOO}bar")
        self.assertEqual(env, {'FOO': 'test', 'BAR': 'testbar'})

    def test_expands_variables_from_environ_if_not_found_in_local_env(self):
        os.environ.setdefault('FOO', 'test')
        env = parse_dotenv('BAR=$FOO')
        self.assertEqual(env, {'BAR': 'test'})

    def test_expands_undefined_variables_to_an_empty_string(self):
        self.assertEqual(parse_dotenv('BAR=$FOO'), {'BAR': ''})

    def test_expands_variables_in_double_quoted_values(self):
        env = parse_dotenv("FOO=test\nBAR=\"quote $FOO\"")
        self.assertEqual(env, {'FOO': 'test', 'BAR': 'quote test'})

    def test_does_not_expand_variables_in_single_quoted_values(self):
        env = parse_dotenv("BAR='quote $FOO'")
        self.assertEqual(env, {'BAR': 'quote $FOO'})

    def test_does_not_expand_escaped_variables(self):
        env = parse_dotenv('FOO="foo\\$BAR"')
        self.assertEqual(env, {'FOO': 'foo$BAR'})

        env = parse_dotenv('FOO="foo\${BAR}"')
        self.assertEqual(env, {'FOO': 'foo${BAR}'})

    def test_parses_export_keyword(self):
        env = parse_dotenv('export FOO=bar')
        self.assertEqual(env, {'FOO': 'bar'})

    def test_parses_key_with_dot_in_the_name(self):
        env = parse_dotenv('FOO.BAR=foobar')
        self.assertEqual(env, {'FOO.BAR': 'foobar'})

    def test_strips_unquoted_values(self):
        env = parse_dotenv('foo=bar ')
        self.assertEqual(env, {'foo': 'bar'})  # not 'bar '

    def test_warns_if_line_format_is_incorrect(self):
        with warnings.catch_warnings(record=True) as w:
            parse_dotenv('lol$wut')

            self.assertEqual(len(w), 1)
            self.assertTrue(w[0].category is SyntaxWarning)
            self.assertEqual(
                str(w[0].message),
                "Line 'lol$wut' doesn't match format"
            )

    def test_ignores_empty_lines(self):
        env = parse_dotenv("\n \t  \nfoo=bar\n \nfizz=buzz")
        self.assertEqual(env, {'foo': 'bar', 'fizz': 'buzz'})

    def test_ignores_inline_comments(self):
        env = parse_dotenv('foo=bar # this is foo')
        self.assertEqual(env, {'foo': 'bar'})

    def test_allows_hash_in_quoted_values(self):
        env = parse_dotenv('foo="bar#baz" # comment ')
        self.assertEqual(env, {'foo': 'bar#baz'})

    def test_ignores_comment_lines(self):
        env = parse_dotenv("\n\n\n # HERE GOES FOO \nfoo=bar")
        self.assertEqual(env, {'foo': 'bar'})

    def test_parses_hash_in_quoted_values(self):
        env = parse_dotenv('foo="ba#r"')
        self.assertEqual(env, {'foo': 'ba#r'})

        env = parse_dotenv('foo="ba#r"')
        self.assertEqual(parse_dotenv("foo='ba#r'"), {'foo': 'ba#r'})


class ReadDotenvTestCase(unittest.TestCase):

    def test_defaults_to_dotenv(self):
        read_dotenv()
        self.assertEqual(os.environ.get('DOTENV'), 'true')

    def test_reads_the_file(self):
        read_dotenv('.env')
        self.assertEqual(os.environ.get('DOTENV'), 'true')

    def test_warns_if_file_does_not_exist(self):
        with warnings.catch_warnings(record=True) as w:
            read_dotenv('.does_not_exist')

            self.assertEqual(len(w), 1)
            self.assertTrue(w[0].category is UserWarning)
            self.assertEqual(
                str(w[0].message),
                "Not reading .does_not_exist - it doesn't exist."
            )

    def test_warns_if_values_not_exist(self):
        with warnings.catch_warnings(record=True) as w:
            read_dotenv('.env', safe=True)

            self.assertEqual(len(w), 1)
            self.assertTrue(w[0].category is UserWarning)
            self.assertEqual(
                str(w[0].message),
                "The following variables were defined in .env.example but "
                "are not present in the environment:\n DOTENV_EXAMPLE"
            )


class ParseDotenvDirectoryTestCase(unittest.TestCase):
    """Test parsing a dotenv file given the directory where it lives"""

    def setUp(self):
        # Define our dotenv directory
        self.dotenv_dir = os.path.join(
            os.path.dirname(__file__), 'dotenv_dir')
        # Create the directory
        os.mkdir(self.dotenv_dir)
        # Copy the test .env file to our new directory
        shutil.copy2(os.path.abspath('.env'), self.dotenv_dir)

    def tearDown(self):
        if os.path.exists(self.dotenv_dir):
            shutil.rmtree(self.dotenv_dir)

    def test_can_read_dotenv_given_its_directory(self):
        read_dotenv(self.dotenv_dir)
        self.assertEqual(os.environ.get('DOTENV'), 'true')


class ReadDotenvExampleTestCase(unittest.TestCase):

    def setUp(self):
        # Define our dotenv directory
        self.dotenv_dir = os.path.join(
            os.path.dirname(__file__), 'dotenv_dir')
        self.dir_not_found = os.path.join(self.dotenv_dir, 'dir_not_found')
        # Create the directories
        os.mkdir(self.dotenv_dir)
        os.mkdir(self.dir_not_found)
        # Copy the test .env file and .env.example file to our new directory
        for file in ('.env', '.env.example'):
            shutil.copy2(os.path.abspath(file), self.dotenv_dir)

    def tearDown(self):
        for dir_name in (self.dotenv_dir, self.dir_not_found):
            if os.path.exists(dir_name):
                shutil.rmtree(dir_name)

    def test_read_example(self):
        dotenv_example = _read_dotenv_example(self.dotenv_dir)
        expected = {'DOTENV': 'true', 'DOTENV_EXAMPLE': 'true'}
        self.assertDictEqual(dotenv_example, expected)

    def test_file_not_exists(self):
        dotenv_example = _read_dotenv_example(self.dir_not_found)
        self.assertDictEqual(dotenv_example, {})


class CheckSafeTestCase(unittest.TestCase):

    def setUp(self):
        # Define our dotenv directory
        self.dotenv_dir = os.path.join(
            os.path.dirname(__file__), 'dotenv_dir')
        # Create the directory
        os.mkdir(self.dotenv_dir)
        # Copy the test .env file to our new directory
        for file in ('.env', '.env.example'):
            shutil.copy2(os.path.abspath(file), self.dotenv_dir)

    def tearDown(self):
        if os.path.exists(self.dotenv_dir):
            shutil.rmtree(self.dotenv_dir)

    def test_return(self):
        dotenv_example = _read_dotenv_example(self.dotenv_dir)
        keys_not_exist = _check_safe(dotenv_example)

        expected = ['DOTENV_EXAMPLE']
        self.assertEqual(keys_not_exist, expected)
