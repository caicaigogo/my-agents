import unittest
from dotenv import load_dotenv
from app.services.llm_service import get_llm
from hello_agents.agents import ToolAwareSimpleAgent
from hello_agents.tools.builtin.calculator import CalculatorTool
from hello_agents.tools import ToolRegistry


class TestSimpleAgent(unittest.TestCase):

    def setUp(self):
        load_dotenv()
        self.llm = get_llm()

        calculate_tool = CalculatorTool()
        tool_registry = ToolRegistry()
        tool_registry.register_tool(calculate_tool)

        system_prompt = '你是能使用tools的人工智能agent'

        self.tool_aware_simple_agent = ToolAwareSimpleAgent(
            name="tool aware simple agent demo",
            llm=self.llm,
            system_prompt=system_prompt,
            tool_registry=tool_registry,
            enable_tool_calling=True
        )

    def test_sanitize_parameters(self):

        parse_tool_parameters = {'expression': '5+3'}
        parse_tool_parameters = self.tool_aware_simple_agent._sanitize_parameters(parse_tool_parameters)

        # {'expression': '5+3'}
        print(parse_tool_parameters)

    def test_tool_listener(self):
        parse_tool_calls = [{'tool_name': 'python_calculator', 'parameters': 'expression=5+3',
                             'original': '[TOOL_CALL:python_calculator:expression=5+3]'}]

        def tool_listener(call_info):
            print(f"工具调用: {call_info['tool_name']}")
            print(f"参数: {call_info['parsed_parameters']}")
            print(f"结果: {call_info['result']}")

        self.tool_aware_simple_agent._tool_call_listener = tool_listener
        call = parse_tool_calls[0]

        # ✅ 工具 'python_calculator' 已注册。
        # 🧮 正在计算: 5+3
        # ✅ 计算结果: 8
        # 工具调用: python_calculator
        # 参数: {'expression': '5+3'}
        # 结果: 🔧 工具 python_calculator 执行结果：
        # 8
        tool_result = self.tool_aware_simple_agent._execute_tool_call(call['tool_name'], call['parameters'])
