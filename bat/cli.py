import argparse
import logging
from logging.config import dictConfig
from sys import exit

from bat.example.cli import example_cli
from bat.logconf import logging_config
from bat.lib import hello_world


dictConfig(logging_config)
log = logging.getLogger('root')


def BATCLI(ARGS=None):
    p = argparser()
    # Execute
    # get only the first command in args
    args = p.parse_args(ARGS)
    Commands.set_log_level(args)
    # execute function set for parsed command
    if not hasattr(Commands, args.func.__name__):
        p.print_help()
        exit(1)
    args.func(args)
    exit(0)


def argparser():
    p = argparse.ArgumentParser(
        description='Utility for executing various bat tasks',
        usage='bat [<args>] <command>',
    )
    p.set_defaults(func=p.print_help)

    p.add_argument(
        '-v', '--verbose',
        help='enable INFO output',
        action='store_const',
        dest='loglevel',
        const=logging.INFO
    )
    p.add_argument(
        '--debug',
        help='enable DEBUG output',
        action='store_const',
        dest='loglevel',
        const=logging.DEBUG,
    )
    p.add_argument(
        '-c', '--conf', '--config_file',
        dest='config_file',
        default=None,
        help='specify a config file to get environment details from',
    )
    p.add_argument(
        '-e', '--env', '--remote_environment',
        dest='remote_environment',
        default=None,
        help='specify the remote environment to use from the config file',
    )

    # Add a subparser to handle sub-commands
    commands = p.add_subparsers(
        dest='command',
        title='commands',
        description='for additonal details on each command use: '
                    '"bat {command name} --help"',
    )
    # hello args
    hello = commands.add_parser(
        'hello',
        description='execute command hello',
        help='for details use hello --help',
    )
    hello.set_defaults(func=Commands.hello)

    server_cli(commands)
    testing_cli(commands)
    # Add a subparser from a module
    example_cli(commands)

    return p


# TODO: Convert this into a ArgumentParser object, and make them composable
def server_cli(subparser):
    server = subparser.add_parser(
        'server',
        usage='bat server [args] <command>',
        help='http server related commands',
        description='http server related commands',
    )

    server.add_argument(
        '-H', '--host', dest='host',
        default='0.0.0.0',
        help='host ip on which the service will be made available',
    )
    server.add_argument(
        '-P', '--port', dest='port',
        default='5000',
        help='port on which the service will be made available'
    )
    server.add_argument(
        '-d', '--debug', dest='debug',
        default=True,
        help='run web service with debug level output'
    )

    server_cmds = server.add_subparsers(
        dest='server_cmds',
        title='server commands',
        help='server control commands',
    )
    # start args
    start = server_cmds.add_parser(
        'start',
        description='start the web server',
        help='for details use start --help',
    )
    start.set_defaults(func=Commands.server_start)

    test = server_cmds.add_parser(
        'test',
        description='run functional tests',
        help='for details use test --help'
    )
    test.set_defaults(func=Commands.server_test)


def testing_cli(subparser):
    # run_functional_tests args
    run_functional_tests = subparser.add_parser(
        'run_functional_tests',
        description='start the server locally and run functional tests',
        help='for details use test --help'
    )
    run_functional_tests.set_defaults(func=Commands.run_functional_tests)
    run_functional_tests.add_argument(
        '-H', '--host', dest='host',
        default='0.0.0.0',
        help='host ip on which the service will be run',
    )
    run_functional_tests.add_argument(
        '-P', '--port', dest='port',
        default='5000',
        help='port on which the service service will be run'
    )

    # run_functional_tests args
    run_container_tests = subparser.add_parser(
        'run_container_tests',
        description='start docker-compose and run functional tests',
        help='for details use test --help'
    )
    run_container_tests.set_defaults(func=Commands.run_container_tests)
    run_container_tests.add_argument(
        '-H', '--host', dest='host',
        default='0.0.0.0',
        help='host ip on which the service will be run',
    )
    run_container_tests.add_argument(
        '-P', '--port', dest='port',
        default='5000',
        help='port on which the service service will be run'
    )


class Commands:

    @staticmethod
    def hello(args):
        print(hello_world())

    @staticmethod
    def set_log_level(args):
        if args.loglevel:
            log.setLevel(args.loglevel)
        else:
            log.setLevel(logging.ERROR)

    @staticmethod
    def server_start(args):
        from bat.server import start_api_server
        start_api_server(host=args.host, port=args.port, debug=args.debug)

    @staticmethod
    def server_test(args):
        print('++ run functional tests ++')
        import unittest
        loader = unittest.TestLoader()
        suite = loader.discover('functional_tests', pattern='*_test.py')
        runner = unittest.TextTestRunner()
        runner.run(suite)

    @staticmethod
    def run_functional_tests(args):
        import subprocess
        import os
        import signal
        from time import sleep
        a = subprocess.Popen(['bat', 'start'])
        sleep(0.5)
        Commands.test(args)

        os.kill(a.pid, signal.SIGTERM)

    @staticmethod
    def run_container_tests(args):
        import subprocess
        import os
        import signal
        from time import sleep
        a = subprocess.Popen(['docker-compose', 'up'])
        sleep(0.5)
        Commands.test(args)

        os.kill(a.pid, signal.SIGTERM)
        sleep(0.5)
