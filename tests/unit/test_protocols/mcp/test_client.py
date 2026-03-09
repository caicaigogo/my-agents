import unittest
from fastmcp import Client, FastMCP


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
        def subtract(a: float, b: float) -> float:
            """减法计算器"""
            return a - b

        @server.tool()
        def multiply(a: float, b: float) -> float:
            """乘法计算器"""
            return a * b

        @server.tool()
        def divide(a: float, b: float) -> float:
            """除法计算器"""
            if b == 0:
                raise ValueError("除数不能为零")
            return a / b

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
    # IsolatedAsyncioTestCase 支持 async def setUp 和 async def test_...

    async def test_FastMCP_source(self):
        # 直接定义为 async，IsolatedAsyncioTestCase 会自动 await 它
        server_source = _create_builtin_server()

        if isinstance(server_source, FastMCP):
            print(f"🧠 使用内存传输：{server_source.name}")

        async with Client(server_source) as client:
            tools = await client.list_tools()
            print("可用工具:", [t.name for t in tools])
