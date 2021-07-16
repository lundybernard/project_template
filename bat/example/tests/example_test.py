from unittest import TestCase
from unittest.mock import patch, Mock
from bat.example.cli import hello_world
from bat.configuration.manager import Configuration

class ExampleTests(TestCase):

    @patch('builtins.print')
    def test_hello_world(t, print):
        conf = Mock(Configuration, autospec=True)
        hello_world(conf)
        print.assert_called_with('Hello from the example module!')
