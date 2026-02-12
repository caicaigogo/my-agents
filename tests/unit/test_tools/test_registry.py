import unittest
from hello_agents.tools.builtin.calculator import CalculatorTool, calculate
from hello_agents.tools import ToolRegistry


class TestToolRegistry(unittest.TestCase):

    def test_register_function(self):

        calculate_tool = CalculatorTool()
        tool_registry = ToolRegistry()

        tool_name = calculate_tool.name
        tool_description = calculate_tool.description

        # 注册计算器函数
        tool_registry.register_function(
            name=tool_name,
            description=tool_description,
            func=calculate
        )
        print(tool_registry._functions)

        self.assertTrue(
            callable(
                tool_registry.get_function(
                    tool_name
                )
            )
        )

        self.assertEqual('11', tool_registry.execute_tool(tool_name, input_text='5+3 * 2'))

        tool_registry.unregister(tool_name)
        self.assertIsNone(
            tool_registry.get_function(tool_name)
        )

    def test_tools_description(self):

        calculate_tool = CalculatorTool()
        tool_registry = ToolRegistry()

        one_tool_name = calculate_tool.name
        one_tool_description = calculate_tool.description

        # 注册计算器函数
        tool_registry.register_function(
            name=one_tool_name,
            description=one_tool_description,
            func=calculate
        )

        tools_description = tool_registry.get_tools_description()
        print(tools_description)
        self.assertNotEqual('暂无可用工具', tools_description)

        tool_registry.unregister(one_tool_name)
        tools_description = tool_registry.get_tools_description()
        self.assertEqual('暂无可用工具', tools_description)
