import unittest
from dotenv import load_dotenv
from hello_agents.tools import CalculatorTool, SearchTool, ToolRegistry, create_simple_chain, create_research_chain


class TestToolChain(unittest.TestCase):
    def setUp(self):

        load_dotenv()

        calculate_tool = CalculatorTool()
        search_tool = SearchTool(backend='tavily')

        tool_registry = ToolRegistry()
        tool_registry.register_tool(calculate_tool)
        tool_registry.register_tool(search_tool)

        self.tool_registry = tool_registry

    def test_create_simple_chain(self):
        simple_chain = create_simple_chain()

        input_data = '5 + 3'
        simple_chain.execute(registry=self.tool_registry, input_data=input_data)

    def test_create_research_chain(self):
        simple_chain = create_research_chain()

        input_data = '特斯拉价格'
        simple_chain.execute(registry=self.tool_registry, input_data=input_data)
