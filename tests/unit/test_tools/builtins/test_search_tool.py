import unittest
import json
from dotenv import load_dotenv

from hello_agents.tools import SearchTool


class TestCalculatorTool(unittest.TestCase):

    def setUp(self):

        load_dotenv()

    def test_tool_run(self):

        search_tool = SearchTool()
        parameters = {
            'input': '特斯拉有几款车型',
            'backend': 'tavily',
            'fetch_full_page': True,
            'mode': 'text'

        }
        text_result = search_tool.run(parameters)
        print('text result \n', text_result)

        parameters = {
            'input': '特斯拉有几款车型',
            'backend': 'tavily',
            'fetch_full_page': True,
            'mode': 'structured'
        }
        structured_result = search_tool.run(parameters)
        print(json.dumps(structured_result, ensure_ascii=False))
