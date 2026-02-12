import unittest
from dotenv import load_dotenv
from app.services.llm_service import get_llm
from hello_agents.agents import SimpleAgent


class TestSimpleAgent(unittest.TestCase):

    def setUp(self):

        load_dotenv()
        self.llm = get_llm()
        self.simple_agent = SimpleAgent(
            name="simple agent demo",
            llm=self.llm,
        )
        print(self.simple_agent)

    def test_llm_history(self):

        init_history = self.simple_agent.get_history()
        self.assertListEqual([], init_history)

        first_query = '你好'
        first_response = self.simple_agent.run(first_query)
        first_round_history = self.simple_agent.get_history()

        self.assertEqual(len(first_round_history), 2)

        first_round_response_message = first_round_history[1]
        first_round_response_dict = first_round_response_message.to_dict()
        self.assertEqual(first_round_response_dict['role'], 'assistant')
        self.assertEqual(first_round_response_dict['content'], first_response)

        second_query = '我刚才说了什么'
        second_response = self.simple_agent.run(second_query)
        second_round_history = self.simple_agent.get_history()

        self.assertEqual(len(second_round_history), 4)

        second_round_response_message = second_round_history[3]

        second_round_response_dict = second_round_response_message.to_dict()

        self.assertEqual(second_round_response_dict['role'], 'assistant')
        self.assertEqual(second_round_response_dict['content'], second_response)

        print(second_response)

        self.simple_agent.clear_history()

        empty_history = self.simple_agent.get_history()
        self.assertEqual(len(empty_history), 0)

        empty_test_query = '我刚才说了什么'
        empty_test_response = self.simple_agent.run(empty_test_query)
        print(empty_test_response)

    def test_system_prompt(self):

        system_prompt = '假装你是个小丑'
        system_check_agent = SimpleAgent(
            name="system_check agent demo",
            llm=self.llm,
            system_prompt=system_prompt
        )
        init_history = system_check_agent.get_history()
        self.assertListEqual([], init_history)

        query = '你是什么'
        response = system_check_agent.run(query)
        print(response)
        self.assertRegex(response, '小丑')
