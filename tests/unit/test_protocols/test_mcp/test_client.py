import unittest
from fastmcp import Client, FastMCP
from fastmcp.client.transports import PythonStdioTransport, SSETransport, StreamableHttpTransport
from dotenv import load_dotenv
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
        load_dotenv()
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

        script_path = 'src/hello_agents/protocols/mcp/server.py'
        print(os.path.exists(script_path))
        server_source = PythonStdioTransport(script_path=script_path)
        print(server_source)

        async with Client(server_source) as client:
            tools = await client.list_tools()
            # 可用工具: ['calculator', 'greet']
            print("可用工具:", [t.name for t in tools])

    async def test_http_source(self):

        url = 'https://api.githubcopilot.com/mcp/'
        github_access_token = os.getenv('GITHUB_ACCESS_TOKEN')
        print(github_access_token)
        headers = {'Authorization': github_access_token}
        server_source = StreamableHttpTransport(url=url, headers=headers)
        print(server_source)

        async with Client(server_source) as client:
            tools = await client.list_tools()
            # 可用工具: ['add_comment_to_pending_review', 'add_issue_comment', 'add_reply_to_pull_request_comment',
            #        'assign_copilot_to_issue', 'create_branch', 'create_or_update_file', 'create_pull_request',
            #        'create_pull_request_with_copilot', 'create_repository', 'delete_file', 'fork_repository',
            #        'get_commit', 'get_copilot_job_status', 'get_file_contents', 'get_label', 'get_latest_release',
            #        'get_me', 'get_release_by_tag', 'get_tag', 'get_team_members', 'get_teams', 'issue_read',
            #        'issue_write', 'list_branches', 'list_commits', 'list_issue_types', 'list_issues',
            #        'list_pull_requests', 'list_releases', 'list_tags', 'merge_pull_request', 'pull_request_read',
            #        'pull_request_review_write', 'push_files', 'request_copilot_review', 'search_code', 'search_issues',
            #        'search_pull_requests', 'search_repositories', 'search_users', 'sub_issue_write',
            #        'update_pull_request', 'update_pull_request_branch']
            print("可用工具:", [t.name for t in tools])


            # 列出可用资源
            resources =await client.list_resources()
            # resources []
            print("resources", resources)

            # 列出可用提示
            # prompts[Prompt(name='AssignCodingAgent', title=None,
            #                description='Assign GitHub Coding Agent to multiple tasks in a GitHub repository.',
            #                arguments=[PromptArgument(name='repo',
            #                                          description='The repository to assign tasks in (owner/repo).',
            #                                          required=True)], icons=[Icon(
            #         src='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABmJLR0QA/wD/AP+gvaeTAAAC2UlEQVRIicWVMUyTaRjHf/+vVUpOJOdilOYoUvVreq2CDmLOwdlAS5xMbrrhBifjYG7QjYuJw108nZx1huLgYlw0QshxChUK2koxHHcuCmgsFfieG0or3kGPSoz/8X3f5/97nvfN8z7wmaVqm9FodFfR/EnMugy5giCAwYwgI9Ff9Hl9L9Lp1zUBgsGO+rqGwnlhF4CdwBSyAUwvS1G220zHBSFgHtmVxYWvfp2ZGSj8LyAcjgfZphTQZtAr7OdsZvSP9RIJR+LtQhcNusF+d1aUfPp05M8NAavmg8AOk3cmN56+s1Hpa7U/cviUYbcw3jgex9ZCKoBgsKM+0PDuAdBq2He5zOiTzZiXtc+NxRw598GeLRcWTuTz+UUAp3ygrqFwHmgzeWdqNQd4PpFOy/gedNQfaDz3UQXRaHRX0fNPGdzNZUZO12q+VuHIoV7g5Hu/1/IinX7tABTNnwR2SvRsxRzAzOsBGuuWfAkoX5FZFzCVHR95tFVAbiI9DEwj6wLwl5YVMTRYLTDsxjuRrgGYYz/kxkbvbXRWMOBB24cKYI9ks1X8hXQDaAaa5XG9WjImZgV71wI+m8qAv8y0t1pSmP0ITANTmHO2qqvRZDALlTdgHKyjWkx2YvQ2cHtTacMxYBhWK5DoF4TCkXj7Jg02VKsbOwI0Y+qvALZrOQXMC13cKkDSJWBuJUCqAhgbG3uF7IpBcn/k8KlPNQ+78U5QQuhy/vHjuQoAYPndwi9gw4bd2ufGYrWatxz8No50ExhaKsz9Vl6vAPL5/KKzoiTGG0fOg1oqCbvxTp/juw/M+zynu/yTwjoD58CBQ02ez/pAR4E+M69ntf3/o1Y3dqR050oAQz7P6Z6cfPRRw647MkOhUMAfaDyH+AloBKYNPRT292rQHoMOSp09J3TZlt5ezWazxX97VR3638RiX9ct+RImSyBcrDT0ETMyMp4ptRIgVX7QL6J/ALSUEwJ5rdg2AAAAAElFTkSuQmCC',
            #         mimeType='image/png', sizes=None, theme='light'), Icon(
            #         src='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABmJLR0QA/wD/AP+gvaeTAAABxElEQVRIibWVvW4TURCFv0vlNEDcIHAkKAERJOIKSjoUArwBPwUFFaKIIngAJARCPIgdh4cgRBYt6ZIAEYEqdhpEw0fhCbkKa68dxyNtsfNzzpnZu3NhwpYGBdUqcA+4A1wEZiK0DawD74FWSml3JAJ1CngGLAIngU1gFfgZKWeAG8AFoAu8At6mlH6VtqTOqJ/UP2pDnRuQO6c27VlbrQ0Dvq121Fulag7q5qPmW18SdSqUd9Qrw4Jn9bNR21YrRQkvYixDKy/AuB3jWjocqKpdtXFU8AxrOTqZzp2PgvnaMRDUA+tB7mypG+OCZ3hbahPgRPguAR9LihaicEu9WcKxClzOi/fU1wPAk7rjgX0uEfNG3cs7mJjtE+wA5/olpZQEHgNf6K2NJyW4NeD7v7c4WptjSc0svlMjdzyM2fbdOyOA7x/T+7mzGj9H8xgIWuquevpw4HmsivkxwBdC/WJRsBKLqqPOHgH8aqybtcJlF0m1WLndUToJ5V31q9r3NOYk7Wh1Wa0PyK3HzA3l/4H3uzIrwFNgCThF7/x/AH5EylngOnAe6AAvgXcppd9DEWRE08DdeIou/RVgJaXUGYQzUfsL+zmwV7BtIq0AAAAASUVORK5CYII=',
            #         mimeType='image/png', sizes=None, theme='dark')], meta=None), Prompt(name='issue_to_fix_workflow',
            #                                                                              title=None,
            #                                                                              description='Create an issue for a problem and then generate a pull request to fix it',
            #                                                                              arguments=[PromptArgument(
            #                                                                                  name='owner',
            #                                                                                  description='Repository owner',
            #                                                                                  required=True),
            #                                                                                         PromptArgument(
            #                                                                                             name='repo',
            #                                                                                             description='Repository name',
            #                                                                                             required=True),
            #                                                                                         PromptArgument(
            #                                                                                             name='title',
            #                                                                                             description='Issue title',
            #                                                                                             required=True),
            #                                                                                         PromptArgument(
            #                                                                                             name='description',
            #                                                                                             description='Issue description',
            #                                                                                             required=True),
            #                                                                                         PromptArgument(
            #                                                                                             name='labels',
            #                                                                                             description='Comma-separated list of labels to apply (optional)',
            #                                                                                             required=None),
            #                                                                                         PromptArgument(
            #                                                                                             name='assignees',
            #                                                                                             description='Comma-separated list of assignees (optional)',
            #                                                                                             required=None)],
            #                                                                              icons=[Icon(
            #                                                                                  src='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABmJLR0QA/wD/AP+gvaeTAAAC2UlEQVRIicWVMUyTaRjHf/+vVUpOJOdilOYoUvVreq2CDmLOwdlAS5xMbrrhBifjYG7QjYuJw108nZx1huLgYlw0QshxChUK2koxHHcuCmgsFfieG0or3kGPSoz/8X3f5/97nvfN8z7wmaVqm9FodFfR/EnMugy5giCAwYwgI9Ff9Hl9L9Lp1zUBgsGO+rqGwnlhF4CdwBSyAUwvS1G220zHBSFgHtmVxYWvfp2ZGSj8LyAcjgfZphTQZtAr7OdsZvSP9RIJR+LtQhcNusF+d1aUfPp05M8NAavmg8AOk3cmN56+s1Hpa7U/cviUYbcw3jgex9ZCKoBgsKM+0PDuAdBq2He5zOiTzZiXtc+NxRw598GeLRcWTuTz+UUAp3ygrqFwHmgzeWdqNQd4PpFOy/gedNQfaDz3UQXRaHRX0fNPGdzNZUZO12q+VuHIoV7g5Hu/1/IinX7tABTNnwR2SvRsxRzAzOsBGuuWfAkoX5FZFzCVHR95tFVAbiI9DEwj6wLwl5YVMTRYLTDsxjuRrgGYYz/kxkbvbXRWMOBB24cKYI9ks1X8hXQDaAaa5XG9WjImZgV71wI+m8qAv8y0t1pSmP0ITANTmHO2qqvRZDALlTdgHKyjWkx2YvQ2cHtTacMxYBhWK5DoF4TCkXj7Jg02VKsbOwI0Y+qvALZrOQXMC13cKkDSJWBuJUCqAhgbG3uF7IpBcn/k8KlPNQ+78U5QQuhy/vHjuQoAYPndwi9gw4bd2ufGYrWatxz8No50ExhaKsz9Vl6vAPL5/KKzoiTGG0fOg1oqCbvxTp/juw/M+zynu/yTwjoD58CBQ02ez/pAR4E+M69ntf3/o1Y3dqR050oAQz7P6Z6cfPRRw647MkOhUMAfaDyH+AloBKYNPRT292rQHoMOSp09J3TZlt5ezWazxX97VR3638RiX9ct+RImSyBcrDT0ETMyMp4ptRIgVX7QL6J/ALSUEwJ5rdg2AAAAAElFTkSuQmCC',
            #                                                                                  mimeType='image/png',
            #                                                                                  sizes=None, theme='light'),
            #                                                                                     Icon(
            #                                                                                         src='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABmJLR0QA/wD/AP+gvaeTAAABxElEQVRIibWVvW4TURCFv0vlNEDcIHAkKAERJOIKSjoUArwBPwUFFaKIIngAJARCPIgdh4cgRBYt6ZIAEYEqdhpEw0fhCbkKa68dxyNtsfNzzpnZu3NhwpYGBdUqcA+4A1wEZiK0DawD74FWSml3JAJ1CngGLAIngU1gFfgZKWeAG8AFoAu8At6mlH6VtqTOqJ/UP2pDnRuQO6c27VlbrQ0Dvq121Fulag7q5qPmW18SdSqUd9Qrw4Jn9bNR21YrRQkvYixDKy/AuB3jWjocqKpdtXFU8AxrOTqZzp2PgvnaMRDUA+tB7mypG+OCZ3hbahPgRPguAR9LihaicEu9WcKxClzOi/fU1wPAk7rjgX0uEfNG3cs7mJjtE+wA5/olpZQEHgNf6K2NJyW4NeD7v7c4WptjSc0svlMjdzyM2fbdOyOA7x/T+7mzGj9H8xgIWuquevpw4HmsivkxwBdC/WJRsBKLqqPOHgH8aqybtcJlF0m1WLndUToJ5V31q9r3NOYk7Wh1Wa0PyK3HzA3l/4H3uzIrwFNgCThF7/x/AH5EylngOnAe6AAvgXcppd9DEWRE08DdeIou/RVgJaXUGYQzUfsL+zmwV7BtIq0AAAAASUVORK5CYII=',
            #                                                                                         mimeType='image/png',
            #                                                                                         sizes=None,
            #                                                                                         theme='dark')],
            #                                                                              meta=None)]
            prompts = await client.list_prompts()
            print("prompts", prompts)
