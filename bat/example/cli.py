import argparse
import textwrap


def example_cli(subparser):
    # Add a subparser to handle sub-commands
    example = subparser.add_parser(
        'example',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help='example cli',
        description=textwrap.dedent('''\
            print the state of the deployment,
            or execute sub commands to manage the deployment:
                bat deployment YYYY-MM-DD {sub command}
        '''),
    )
    # A required argument
    example.add_argument(
        dest='date',
        default="(YYYY-MM-DD)",
        help='Date of deployment (YYYY-MM-DD)',
    )
    # Default behavior if no sub-command is given
    example.set_defaults(func=default)
    # Add additional sub-commands to this cli
    example_cmds = example.add_subparsers(
        dest='example_cmds',
        title='example commands',
        description='for additonal details on each command use: '
        '"bat example x {command name} --help"',
    )
    hello = example_cmds.add_parser(
        'hello',
        help='say hello',
        description='hello world from the example module',
    )
    hello.set_defaults(func=hello_world)

    return subparser


def default(args):
    print('default response from example module CLI')


def hello_world(args):
    print('Hello from the example module!')
