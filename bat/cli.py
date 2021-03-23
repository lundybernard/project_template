import argparse
import logging
from logging.config import dictConfig
from sys import exit

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
        usage='bat [<args>] <command>'
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
        help='specify the remote environment to use fromthe config file',
    )

    # Add a subparser to handle sub-commands
    commands = p.add_subparsers(
        dest='command',
        title='commands',
        description='valid commands',
    )
    # hello args
    hello = commands.add_parser(
        'hello',
        description='execute command hello',
        help='for details use hello --help',
    )
    hello.set_defaults(func=Commands.hello)

    # start args
    start = commands.add_parser(
        'start',
        description='start the web server',
        help='for details use start --help',
    )
    start.set_defaults(func=Commands.start)
    start.add_argument(
        '-H', '--host', dest='host',
        default='0.0.0.0',
        help='host ip on which the service will be made available',
    )
    start.add_argument(
        '-P', '--port', dest='port',
        default='5000',
        help='port on which the service will be made available'
    )
    start.add_argument(
        '-d', '--debug', dest='debug',
        default=True,
        help='run web service with debug level output'
    )

    # test args
    test = commands.add_parser(
        'test',
        description='run functional tests',
        help='for details use test --help'
    )
    test.set_defaults(func=Commands.test)
    test.add_argument(
        '-H', '--host', dest='host',
        default='0.0.0.0',
        help='host ip on which the service is running',
    )
    test.add_argument(
        '-P', '--port', dest='port',
        default='5000',
        help='port on which the service is running'
    )

    # run_functional_tests args
    run_functional_tests = commands.add_parser(
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
    run_container_tests = commands.add_parser(
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

    # example sub command
    sub1 = commands.add_parser(
        'sub1',
        description='execute command sub1',
        help='for details use sub1 --help'
    )
    sub1.set_defaults(func=Commands.sub1)

    sub1.add_argument(
        '-a', '--argument',
        dest='argument',
        default=None,
        help='tell me what arg1 does',
    )

    return p


class Commands:

    @staticmethod
    def set_log_level(args):
        if args.loglevel:
            log.setLevel(args.loglevel)
        else:
            log.setLevel(logging.ERROR)

    @staticmethod
    def start(args):
        from bat.server import start_server
        start_server(host=args.host, port=args.port, debug=args.debug)

    @staticmethod
    def test(args):
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

    @staticmethod
    def hello(args):
        print(hello_world())

    @staticmethod
    def sub1(args):
        print('sub1 example command')
