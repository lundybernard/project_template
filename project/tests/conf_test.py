from unittest import TestCase, mock

from project.conf import get_config


SRC = 'project.conf'


class TestConfiguration(TestCase):

    def test_get_config_loads_given_config_file(t):
        CONF = get_config('./example.config.yaml')
        example_env = CONF['example']

        t.assertEqual(
            example_env['remote_host']['api_key'],
            'example_api_key'
        )
        t.assertEqual(
            example_env['remote_host']['url'],
            'https://api-example.host.io/'
        )

    def test_config_default_environment(t):
        CONF = get_config('./example.config.yaml')

        t.assertEqual(CONF['default'], 'example')

        default_env = CONF[CONF['default']]

        t.assertEqual(
            default_env['remote_host']['api_key'],
            CONF['example']['remote_host']['api_key']
        )
        t.assertEqual(
            default_env['remote_host']['url'],
            CONF['example']['remote_host']['url']
        )

    @mock.patch.dict(
        f'{SRC}.os.environ', {'PROJECT_CONFIG': 'example.config.yaml'}
    )
    def test_config_file_env_variable(t):
        CONF = get_config()

        example_env = CONF['example']
        t.assertEqual(
            example_env['remote_host']['api_key'],
            'example_api_key'
        )
        t.assertEqual(
            example_env['remote_host']['url'],
            'https://api-example.host.io/'
        )

    @mock.patch.dict(f'{SRC}.os.environ', {}, clear=True)
    def test_config_missing_file(t):
        '''PROJECT_CONFIG is not set
        '''
        with t.assertRaises(Exception):
            get_config()
