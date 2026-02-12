import unittest
from dotenv import load_dotenv
from app.services.llm_service import get_llm
from hello_agents.tools.builtin.calculator import CalculatorTool, calculate
from hello_agents.agents import SimpleAgent
from hello_agents.tools import ToolRegistry


class TestCalculatorTool(unittest.TestCase):

    def setUp(self):

        load_dotenv()
        self.llm = get_llm()

    def test_calculate_function(self):

        self.assertEqual('5', calculate('5'))
        self.assertEqual('8', calculate('5+3'))
        self.assertEqual('15', calculate('5 * 3'))
        self.assertEqual('1.2', calculate('6/5'))
        self.assertEqual('8', calculate('2**3'))
        self.assertEqual('0', calculate('1^1'))

        self.assertEqual('-1', calculate('-1'))

        self.assertEqual('5', calculate('abs(-5)'))
        self.assertEqual('3', calculate('round(3.4)'))
        self.assertEqual('4', calculate('round(3.5)'))

        self.assertEqual('8', calculate('max(3, -1, 8)'))
        self.assertEqual('-1', calculate('min(3, -1, 8)'))
        self.assertEqual('0.4', calculate('sqrt(0.16)'))
        self.assertEqual('0.0', calculate('sin(0)'))
        self.assertEqual('1.0', calculate('cos(0)'))
        self.assertEqual('0.0', calculate('tan(0)'))
        self.assertEqual('0.0', calculate('log(1)'))
        self.assertEqual('1.0', calculate('exp(0)'))
        self.assertEqual('3.141592653589793', calculate('pi'))
        self.assertEqual('2.718281828459045', calculate('e'))

    def test_tool_invoke(self):

        calculate_tool = CalculatorTool()
        tool_registry = ToolRegistry()
        tool_registry.register_tool(calculate_tool)

        system_prompt = '你是能使用tools的人工智能agent'

        tool_invoke_agent = SimpleAgent(
            name="function agent demo",
            llm=self.llm,
            system_prompt=system_prompt,
            tool_registry=tool_registry,
            enable_tool_calling=True
        )

        user_query = '请帮忙计算下 5+3'
        # glm-4-flash: python_calculator\n5+3
        # 指令跟随能力不强

        # glm-4.7-flash -> `[TOOL_CALL:python_calculator:expression=5+3]`
        # glm-4.7-flash, 指令跟随能力有进步，但是多了参数名 expression

        tool_invoke_agent.run(user_query)
        print(tool_invoke_agent.get_history())
