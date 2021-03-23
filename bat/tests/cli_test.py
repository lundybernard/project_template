from unittest import TestCase
from unittest.mock import patch

from ..cli import (
    argparser,
    BATCLI,
    Commands,
    logging,
    argparse,
)


SRC = 'bat.cli'


class TestArgparser(TestCase):

    def test_argparser(t):
        argparser()


class TestBATCLI(TestCase):

    def setUp(t):
        patches = ['exit', ]
        for target in patches:
            patcher = patch(f'{SRC}.{target}', autospec=True)
            setattr(t, target, patcher.start())
            t.addCleanup(patcher.stop)

    @patch(f'{SRC}.Commands.set_log_level', autospec=True)
    def test_set_log_level(t, set_log_level):
        args = ['--debug', 'hello', ]
        BATCLI(args)
        set_log_level.assert_called_with(argparser().parse_args(args))
        t.exit.assert_called_with(0)

    def test_commands(t):
        commands = [
            'hello',
            'start',
            'test',
            'run_functional_tests',
            'run_container_tests',
        ]

        for cmd in commands:
            with t.subTest(cmd):
                with patch(f'{SRC}.Commands.{cmd}', autospec=True) as m_cmd:
                    m_cmd.__name__ = cmd
                    args = [cmd, ]
                    BATCLI(args)
                    m_cmd.assert_called_with(argparser().parse_args(args))
                    t.exit.assert_called_with(0)

    # TODO: full coverage of CLI arguments that trigger commands


class TestCommands(TestCase):

    @patch(f'{SRC}.log', autospec=True)
    def test_set_log_level(t, log):
        with t.subTest('default to ERROR'):
            args = argparse.Namespace(loglevel=logging.INFO)
            Commands.set_log_level(args)
            log.setLevel.assert_called_with(logging.INFO)

        with t.subTest('set given value'):
            args = argparse.Namespace(loglevel=logging.INFO)
            Commands.set_log_level(args)
            log.setLevel.assert_called_with(logging.INFO)
