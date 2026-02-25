import unittest
from dotenv import load_dotenv
from hello_agents.tools import CalculatorTool, ToolRegistry, run_parallel_tools
import asyncio


class TesAsyncToolExecutor(unittest.TestCase):
    def setUp(self):

        load_dotenv()
        tool_registry = ToolRegistry()

        calculate_tool = CalculatorTool()
        tool_registry.register_tool(calculate_tool)

        self.tool_registry = tool_registry

    def test_run_parallel_tools(self):
        # 示例函数
        async def demo_parallel_execution():
            """演示并行执行的示例"""

            # 定义并行任务
            tasks = [
                {"tool_name": "python_calculator", "input_data": "2 + 2"},
                {"tool_name": "python_calculator", "input_data": "3 * 4"},
                {"tool_name": "python_calculator", "input_data": "sqrt(16)"},
                {"tool_name": "python_calculator", "input_data": "10 / 2"},
            ]

            # 并行执行
            results = await run_parallel_tools(self.tool_registry, tasks)

            # 显示结果
            print("\n📊 并行执行结果:")
            for result in results:
                status_icon = "✅" if result["status"] == "success" else "❌"
                print(f"{status_icon} {result['tool_name']}({result['input_data']}) = {result['result']}")

            return results

        # 运行演示
        asyncio.run(demo_parallel_execution())

