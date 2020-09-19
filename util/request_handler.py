import os
import requests


class RequestHandler:
    def __init__(self):
        self.session_eth = requests.Session()
        self.session_payment = requests.Session()
        self.eth_proxy_host = os.environ.get('ETH_PROXY_HOST', 'localhost')
        self.payment_processor_host = os.environ.get('PAYMENT_PROCESSOR_HOST', 'localhost')

    def get_project(self):
        return self.session_payment.get('http://{}/create_project'.format(self.payment_processor_host)).json()

    def post_eth_proxy(self, method, params):
        return self.session_eth.post('http://{}/'.format(self.eth_proxy_host), data={
            'method': 'passthrough',
            'params': {
                'method': method,
                'params': params
            }
        }).json()
