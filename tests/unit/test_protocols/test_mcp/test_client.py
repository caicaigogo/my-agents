import unittest
from fastmcp import Client, FastMCP
from fastmcp.client.transports import PythonStdioTransport, SSETransport, StreamableHttpTransport

import os
from pathlib import Path


def find_project_root_with_tests(start_path=None):
    """
    从 start_path 开始向上查找，直到找到包含 'tests' 目录的父目录。
    返回该父目录的 Path 对象。
    如果没找到，抛出 FileNotFoundError。
    """
    if start_path is None:
        start_path = Path.cwd()
    else:
        start_path = Path(start_path).resolve()

    # 限制向上查找，避免无限循环（比如到根目录为止）
    for parent in [start_path] + list(start_path.parents):
        if (parent / "tests").is_dir():
            return parent

    raise FileNotFoundError("未找到包含 'tests' 目录的项目根目录")


def _create_builtin_server():
    """创建内置演示服务器"""
    try:
        from fastmcp import FastMCP

        server = FastMCP("HelloAgents-BuiltinServer")

        @server.tool()
        def add(a: float, b: float) -> float:
            """加法计算器"""
            return a + b

        @server.tool()
        def greet(name: str = "World") -> str:
            """友好问候"""
            return f"Hello, {name}! 欢迎使用 HelloAgents MCP 工具！"

        @server.tool()
        def get_system_info() -> dict:
            """获取系统信息"""
            import platform
            import sys
            return {
                "platform": platform.system(),
                "python_version": sys.version,
                "server_name": "HelloAgents-BuiltinServer",
                "tools_count": 6
            }

        # 2.1 静态文本资源
        @server.resource("config://app/settings")
        def get_settings() -> str:
            """返回应用配置"""
            return '{"theme": "dark", "language": "zh-CN"}'

        # 3.1 基础提示
        @server.prompt("code_review")
        def code_review_prompt() -> str:
            """代码审查提示"""
            return "请审查以下代码，关注性能、安全性和可维护性："

        return server

    except ImportError:
        raise ImportError(
            "创建内置 MCP 服务器需要 fastmcp 库。请安装: pip install fastmcp"
        )


# class TestMCPClient(unittest.TestCase):
#
#     def setUp(self):
#
#         load_dotenv()
#
#     async def test_FastMCP_source(self):
#         # 示例：创建一个简单的 MCP 服务器
#         server_source = _create_builtin_server()
#
#         # 1. FastMCP 实例 - 内存传输
#         if isinstance(server_source, FastMCP):
#             print(f"🧠 使用内存传输: {server_source.name}")
#
#         # client = Client(server_source)
#         # #<coroutine object Client.list_tools at 0x00000249A294A960>
#         # print(client.list_tools())
#
#         async with Client(server_source) as client:
#             # 列出可用工具
#             tools = await client.list_tools()
#             print("可用工具:", [t.name for t in tools])


class TestMCPClient(unittest.IsolatedAsyncioTestCase):
    # IsolatedAsyncioTestCase 支持
    def setUp(self):
        project_root = find_project_root_with_tests()
        os.chdir(project_root)

    async def test_FastMCP_source(self):
        # 直接定义为 async，IsolatedAsyncioTestCase 会自动 await 它
        server_source = _create_builtin_server()

        if isinstance(server_source, FastMCP):
            print(f"🧠 使用内存传输：{server_source.name}")

        async with Client(server_source) as client:

            tools = await client.list_tools()
            # 可用工具: ['add', 'subtract', 'multiply', 'divide', 'greet', 'get_system_info']
            print("可用工具:", [t.name for t in tools])

            arguments = {'a': 5, 'b': 3}

            # call_results CallToolResult(content=[TextContent(type='text', text='8.0', annotations=None, meta=None)],
            # structured_content={'result': 8.0}, meta=None, data=8.0, is_error=False)
            call_results = await client.call_tool('add', arguments=arguments)
            print("call_results", call_results)

            # call_results CallToolResult(content=[TextContent(type='text', text='{"platform":"Windows",
            # "python_version":"3.10.11 (tags/v3.10.11:7d4cc5a, Apr  5 2023, 00:38:17)
            # [MSC v.1929 64 bit (AMD64)]","server_name":"HelloAgents-BuiltinServer","tools_count":6}',
            # annotations=None, meta=None)], structured_content={'platform': 'Windows',
            # 'python_version': '3.10.11 (tags/v3.10.11:7d4cc5a, Apr  5 2023, 00:38:17) [MSC v.1929 64 bit (AMD64)]',
            # 'server_name': 'HelloAgents-BuiltinServer', 'tools_count': 6}, meta=None,
            # data={'platform': 'Windows', 'python_version': '3.10.11 (tags/v3.10.11:7d4cc5a, Apr  5 2023, 00:38:17)
            # [MSC v.1929 64 bit (AMD64)]',
            # 'server_name': 'HelloAgents-BuiltinServer', 'tools_count': 6}, is_error=False)
            call_results = await client.call_tool('get_system_info')
            print("call_results", call_results)

            # 列出可用资源
            resources =await client.list_resources()

            # [Resource(name='get_settings', title=None, uri=AnyUrl('config://app/settings'),
            # description='返回应用配置', mimeType='text/plain', size=None, icons=None, annotations=None,
            # meta={'_fastmcp': {'tags': []}})]
            print("resources", resources)


            # 读取特定资源
            # 配置内容: [TextResourceContents(uri=AnyUrl('config://app/settings'),
            # mimeType='text/plain', meta=None, text='{"theme": "dark", "language": "zh-CN"}')]
            content = await client.read_resource("config://app/settings")
            print("配置内容:", content)

            # 列出可用提示
            prompts = await client.list_prompts()
            # prompts [Prompt(name='code_review', title=None, description='代码审查提示',
            # arguments=[], icons=None, meta={'_fastmcp': {'tags': []}})]
            print("prompts", prompts)

            # 获取提示内容
            # 提示内容：meta=None description='代码审查提示' messages=[PromptMessage(role='user',
            # content=TextContent(type='text',
            # text='请审查以下代码，关注性能、安全性和可维护性：', annotations=None, meta=None))]
            prompt = await client.get_prompt("code_review")
            print(f"提示内容：{prompt}")

    async def test_python_source(self):
        # 直接定义为 async，IsolatedAsyncioTestCase 会自动 await 它

        script_path = 'src/hello_agents/protocols/mcp/server.py'
        print(os.path.exists(script_path))
        server_source = PythonStdioTransport(script_path=script_path)
        print(server_source)

        async with Client(server_source) as client:
            print('enter')
            tools = await client.list_tools()
            print("可用工具:", [t.name for t in tools])
