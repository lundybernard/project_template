import argparse
import logging
from logging.config import dictConfig

from project.lib import hello_world


# === LOGGING === #
logging_config = dict(
    version=1,
    formatters={
        'f': {'format':
              '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'},
        'thread_formatter': {
            'format':
            '%(asctime)s %(threadName)-12s %(levelname)-8s %(message)s'
        }
    },
    handlers={
        'h': {
            'class': 'logging.StreamHandler',
            'formatter': 'f'
        },
        'thread_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'thread_formatter'
        }
    },
    loggers={
        'root': {
            'handlers': ['h'],
            'level': logging.DEBUG
        },
        'mod': {
            'handlers': ['h'],
            'level': logging.DEBUG
        },
        'thread': {
            'handlers': ['thread_handler'],
            'level': logging.DEBUG
        }
    }
)


dictConfig(logging_config)
log = logging.getLogger('root')


class ProjectCLI(object):

    def __init__(self):
        p = argparse.ArgumentParser(
            description='Utility for executing various pytorch_server tasks',
            usage='pytorch_server [<args>] <command>'
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
        hello.set_defaults(func=self.hello)

        # start args
        start = commands.add_parser(
            'start',
            description='start the web server',
            help='for details use start --help',
        )
        start.set_defaults(func=self.start)
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
        test.set_defaults(func=self.test)
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
        run_functional_tests.set_defaults(func=self.run_functional_tests)
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
        run_container_tests.set_defaults(func=self.run_container_tests)
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
        sub1.set_defaults(func=self.sub1)

        sub1.add_argument(
            '-a', '--argument',
            dest='argument',
            default=None,
            help='tell me what arg1 does',
        )

        # Execute
        # get only the first command in args
        args = p.parse_args()
        self.set_log_level(args)
        # execute function set for parsed command
        if not hasattr(self, args.func.__name__):
            p.print_help()
            exit(1)
        args.func(args)
        exit(0)

    def set_log_level(self, args):
        if args.loglevel:
            log.setLevel(args.loglevel)
        else:
            log.setLevel(logging.ERROR)

    def start(self, args):
        from project.server import start_server
        start_server(host=args.host, port=args.port, debug=args.debug)

    def test(self, args):
        print('++ run functional tests ++')
        import unittest
        loader = unittest.TestLoader()
        suite = loader.discover('functional_tests', pattern='*_test.py')
        runner = unittest.TextTestRunner()
        runner.run(suite)

    def run_functional_tests(self, args):
        import subprocess
        import os
        import signal
        from time import sleep
        a = subprocess.Popen(['project', 'start'])
        sleep(0.5)
        self.test(args)

        os.kill(a.pid, signal.SIGTERM)

    def run_container_tests(self, args):
        import subprocess
        import os
        import signal
        from time import sleep
        a = subprocess.Popen(['docker-compose', 'up'])
        sleep(0.5)
        self.test(args)

        os.kill(a.pid, signal.SIGTERM)
        sleep(0.5)

    def hello(self, args):
        print(hello_world())

    def sub1(self, args):
        print('sub1 example command')
