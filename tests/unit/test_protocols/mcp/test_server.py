import unittest
import sys


class TestMCPServer(unittest.TestCase):

    def setUp(self):

        # from hello_agents.protocols.mcp.server import create_example_server
        # 先执行create_example_server 启动mcp服务
        # 如果在untests执行的话

        # 在测试环境（如 pytest）中，sys.stdout 被重定向为 FlushingStringIO 对象，而该对象没有 buffer 属性，
        # 导致访问 sys.stdout.buffer 时抛出 AttributeError。
        # stdout 类型：<class 'teamcity.common.FlushingStringIO'>
        print(f"stdout 类型：{type(sys.stdout)}")

