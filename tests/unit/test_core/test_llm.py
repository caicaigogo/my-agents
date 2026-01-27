import os
import unittest
from dotenv import load_dotenv
from hello_agents import HelloAgentsLLM
from collections.abc import Iterator


class TestHelloAgentsLLM(unittest.TestCase):

    def setUp(self):
        load_dotenv()
        self.original_env = {
            'LLM_MODEL_ID': os.getenv('LLM_MODEL_ID'),
            'LLM_API_KEY': os.getenv('LLM_API_KEY'),
            'LLM_BASE_URL': os.getenv('LLM_BASE_URL'),
            'LLM_TIMEOUT': os.getenv('LLM_TIMEOUT')
        }
        self.llm = HelloAgentsLLM()
        demo_messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "你好"}
        ]
        self.messages = demo_messages

    def test_invoke(self):

        response = self.llm.invoke(self.messages)
        self.assertIsInstance(response, str)

    def test_stream_invoke(self):

        response = self.llm.stream_invoke(self.messages)
        self.assertIsInstance(response, Iterator)
        for _ in response:
            pass
