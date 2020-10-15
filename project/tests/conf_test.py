from unittest import TestCase

from ..conf import get_config


class TestConfiguration(TestCase):

    def test_get_config_loads_given_config_file(t):
        CONF = get_config('./example_conf.yaml')
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
        CONF = get_config('./example_conf.yaml')

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
