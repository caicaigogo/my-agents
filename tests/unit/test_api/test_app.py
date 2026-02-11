import os
import json
import unittest
from dotenv import load_dotenv
import http.client


class TestHelloAgentsLLM(unittest.TestCase):

    def setUp(self):
        load_dotenv()

    def test_health(self):

        host = os.getenv('PUBLIC_HOST')

        conn = http.client.HTTPConnection(host, 8000)
        payload = ''
        headers = {}
        conn.request("GET", "/health", payload, headers)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        self.assertEqual(data['status'], 'healthy')
