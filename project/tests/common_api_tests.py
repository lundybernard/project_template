import requests

PT_SVC_ADDR = 'http://0.0.0.0:5000/'


class CommonAPITest(object):
    '''Define the API tests in their own inheritable class
    so they may be reused in multiple test cases.
    This was done to allow testing of the api in a container
    and as local service.
    '''

    def test_compose_webservice_exists(self):
        out = requests.get(self.service_address)
        self.assertEqual(out.text, 'Hello World!')
