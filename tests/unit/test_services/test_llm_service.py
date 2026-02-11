import unittest
from dotenv import load_dotenv
from app.services.llm_service import get_llm, reset_llm
from hello_agents import HelloAgentsLLM


class TestLLMService(unittest.TestCase):

    def setUp(self):

        load_dotenv()

    def test_llm_get_reset(self):
        from app.services.llm_service import _llm_instance
        self.assertIsNone(_llm_instance)

        get_llm()

        from app.services.llm_service import _llm_instance
        self.assertIsInstance(_llm_instance, HelloAgentsLLM)

        reset_llm()
        from app.services.llm_service import _llm_instance
        self.assertIsNone(_llm_instance)
