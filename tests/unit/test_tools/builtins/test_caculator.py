import unittest
from dotenv import load_dotenv
from app.services.llm_service import get_llm
from hello_agents.tools.builtin.calculator import CalculatorTool, calculate
from hello_agents.agents import SimpleAgent
from hello_agents.tools import ToolRegistry, ToolParameter


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

    def test_tool_run(self):

        calculate_tool = CalculatorTool()
        parameters = {'input': '5+3'}
        result = calculate_tool.run(parameters)
        self.assertEqual('8', result)

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
        # [{'role': 'system', 'content': '你是能使用tools的人工智能agent\n\n## 可用工具\n你可以使用以下工具来帮助回答问题：\n- python_calculator: 执行数学计算。支持基本运算、数学函数等。例如：2+3*4, sqrt(16), sin(pi/2)等。\n\n## 工具调用格式\n当需要使用工具时，请使用以下格式：\n`[TOOL_CALL:{tool_name}:{parameters}]`\n\n### 参数格式说明\n1. **多个参数**：使用 `key=value` 格式，用逗号分隔\n   示例：`[TOOL_CALL:calculator_multiply:a=12,b=8]`\n   示例：`[TOOL_CALL:filesystem_read_file:path=README.md]`\n\n2. **单个参数**：直接使用 `key=value`\n   示例：`[TOOL_CALL:search:query=Python编程]`\n\n3. **简单查询**：可以直接传入文本\n   示例：`[TOOL_CALL:search:Python编程]`\n\n### 重要提示\n- 参数名必须与工具定义的参数名完全匹配\n- 数字参数直接写数字，不需要引号：`a=12` 而不是 `a="12"`\n- 文件路径等字符串参数直接写：`path=README.md`\n- 工具调用结果会自动插入到对话中，然后你可以基于结果继续回答\n'}, {'role': 'user', 'content': '请帮忙计算下 5+3'}, {'role': 'assistant', 'content': '``'}, {'role': 'user', 'content': '工具执行结果：\n🔧 工具 python_calculator 执行结果：\n8\n\n请基于这些结果给出完整的回答。'}]
        # [Message(content='请帮忙计算下 5+3', role='user', timestamp=datetime.datetime(2026, 2, 13, 8, 17, 53, 715086), metadata={}), Message(content='5+3 = 8\n\n计算结果为 8。', role='assistant', timestamp=datetime.datetime(2026, 2, 13, 8, 17, 53, 715086), metadata={})]
        # [Message(content='请帮忙计算下 5+3', role='user', timestamp=datetime.datetime(2026, 2, 13, 8, 20, 1, 863031), metadata={}), Message(content='5+3 的计算结果是 **8**。\n\n我使用了 python_calculator 工具进行了计算，得到了正确的结果。', role='assistant', timestamp=datetime.datetime(2026, 2, 13, 8, 20, 1, 863031), metadata={})]
        print(tool_invoke_agent.get_history())

    def test_tool_parameter(self):

        calculate_tool = CalculatorTool()
        parameters = calculate_tool.get_parameters()
        self.assertIsInstance(parameters[0], ToolParameter)
        print(parameters)
