from unittest import TestCase

from project.lib import hello_world


class ProjectTests(TestCase):

    def test_project(t):
        ret = hello_world()
        t.assertEqual(ret, 'Hello World!')
