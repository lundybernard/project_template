import argparse
import textwrap


def get_help(parser):
    def help(args):
        parser.print_help()
    return help


def example_cli():
    example = argparse.ArgumentParser(
        prog='example',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            print the state of the deployment,
            or execute sub commands to manage the deployment:
                bat deployment YYYY-MM-DD {sub command}
        '''),
    )
    # Default behavior if no sub-command is given
    # example.set_defaults(func=get_help(example))
    example.set_defaults(func=default)

    # A required argument
    example.add_argument(
        dest='date',
        default="(YYYY-MM-DD)",
        help='Date of deployment (YYYY-MM-DD)',
    )

    # Add additional sub-commands to this cli
    commands = example.add_subparsers(
        dest='example_cmds',
        title='example commands',
        description='for additonal details on each command use: '
        '"bat example x {command name} --help"',
    )

    hello = commands.add_parser(
        'hello',
        help='say hello',
        description='hello world from the example module',
    )
    hello.set_defaults(func=hello_world)

    return example


def default(args):
    print('default response from example module CLI')


def hello_world(args):
    print('Hello from the example module!')
