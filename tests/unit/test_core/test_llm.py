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
        use_third_party = False
        if use_third_party:
            self.llm = HelloAgentsLLM()
        else:
            provider = 'custom'
            model = 'qwen2.5:0.5b'
            public_host = os.getenv('PUBLIC_HOST')
            base_url = "http://{}:11434/v1".format(public_host)
            self.llm = HelloAgentsLLM(model=model, base_url=base_url, provider=provider)

        demo_messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "你好"}
        ]
        self.messages = demo_messages

    def test_invoke(self):

        response = self.llm.invoke(self.messages)
        print(response)
        self.assertIsInstance(response, str)

    def test_max_token_invoke(self):
        max_tokens = 5
        response = self.llm._client.chat.completions.create(
            model=self.llm.model,
            messages=self.messages,
            max_tokens=max_tokens
        )
        usage = response.usage
        completion_tokens = usage.completion_tokens
        # prompt_tokens = usage.prompt_tokens
        # total_tokens = usage.total_tokens
        self.assertEqual(completion_tokens, max_tokens)

    def test_stream_invoke(self):

        response = self.llm.stream_invoke(self.messages)
        print(response)
        self.assertIsInstance(response, Iterator)
        for _ in response:
            pass
