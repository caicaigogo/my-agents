import unittest
from dotenv import load_dotenv
from app.services.llm_service import get_llm
from hello_agents.agents import SimpleAgent
from hello_agents.tools.builtin.calculator import CalculatorTool, calculate
from hello_agents.tools import ToolRegistry


class TestSimpleAgent(unittest.TestCase):

    def setUp(self):

        load_dotenv()
        self.llm = get_llm()

    def test_llm_history(self):

        simple_agent = SimpleAgent(
            name="simple agent demo",
            llm=self.llm,
        )
        print(simple_agent)

        init_history = simple_agent.get_history()
        self.assertListEqual([], init_history)

        first_query = '你好'
        first_response = simple_agent.run(first_query)
        first_round_history = simple_agent.get_history()

        self.assertEqual(len(first_round_history), 2)

        first_round_response_message = first_round_history[1]
        first_round_response_dict = first_round_response_message.to_dict()
        self.assertEqual(first_round_response_dict['role'], 'assistant')
        self.assertEqual(first_round_response_dict['content'], first_response)

        second_query = '我刚才说了什么'
        second_response = simple_agent.run(second_query)
        second_round_history = simple_agent.get_history()

        self.assertEqual(len(second_round_history), 4)

        second_round_response_message = second_round_history[3]

        second_round_response_dict = second_round_response_message.to_dict()

        self.assertEqual(second_round_response_dict['role'], 'assistant')
        self.assertEqual(second_round_response_dict['content'], second_response)

        print(second_response)

        simple_agent.clear_history()

        empty_history = simple_agent.get_history()
        self.assertEqual(len(empty_history), 0)

        empty_test_query = '我刚才说了什么'
        empty_test_response = simple_agent.run(empty_test_query)
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

    def test_function_prompt(self):

        calculate_tool = CalculatorTool()
        one_tool_name = calculate_tool.name
        one_tool_description = calculate_tool.description

        tool_registry = ToolRegistry()

        # 注册计算器函数
        tool_registry.register_function(
            name=one_tool_name,
            description=one_tool_description,
            func=calculate
        )

        system_prompt = '你是能使用tools的人工智能agent'

        function_agent = SimpleAgent(
            name="function agent demo",
            llm=self.llm,
            system_prompt=system_prompt,
            tool_registry=tool_registry,
            enable_tool_calling=True
        )

        enhance_tool_system_prompt = function_agent._get_enhanced_system_prompt()

        # 你是能使用tools的人工智能agent

        # ## 可用工具
        # 你可以使用以下工具来帮助回答问题：
        # - python_calculator: 执行数学计算。支持基本运算、数学函数等。例如：2+3*4, sqrt(16), sin(pi/2)等。

        # ## 工具调用格式
        # 当需要使用工具时，请使用以下格式：
        # `[TOOL_CALL:{tool_name}:{parameters}]`

        # ### 参数格式说明
        # 1. **多个参数**：使用 `key=value` 格式，用逗号分隔
        #    示例：`[TOOL_CALL:calculator_multiply:a=12,b=8]`
        #    示例：`[TOOL_CALL:filesystem_read_file:path=README.md]`

        # 2. **单个参数**：直接使用 `key=value`
        #    示例：`[TOOL_CALL:search:query=Python编程]`

        # 3. **简单查询**：可以直接传入文本
        #    示例：`[TOOL_CALL:search:Python编程]`

        # ### 重要提示
        # - 参数名必须与工具定义的参数名完全匹配
        # - 数字参数直接写数字，不需要引号：`a=12` 而不是 `a="12"`
        # - 文件路径等字符串参数直接写：`path=README.md`
        # - 工具调用结果会自动插入到对话中，然后你可以基于结果继续回答

        print(enhance_tool_system_prompt)
        self.assertTrue(one_tool_name in enhance_tool_system_prompt)
        self.assertTrue(one_tool_description in enhance_tool_system_prompt)
