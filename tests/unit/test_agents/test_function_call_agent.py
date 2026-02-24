import unittest
from dotenv import load_dotenv
from app.services.llm_service import get_llm
from hello_agents.agents import FunctionCallAgent
from hello_agents.tools.builtin.calculator import CalculatorTool
from hello_agents.tools import ToolRegistry


class TestFunctionCallAgent(unittest.TestCase):

    def setUp(self):
        load_dotenv()
        self.llm = get_llm()

        calculate_tool = CalculatorTool()
        tool_registry = ToolRegistry()
        tool_registry.register_tool(calculate_tool)

        system_prompt = '你是能使用tools的人工智能agent'

        self.function_call_agent = FunctionCallAgent(
            name="function call agent demo",
            llm=self.llm,
            system_prompt=system_prompt,
            tool_registry=tool_registry,
            enable_tool_calling=True
        )

    def test_invoke_with_tools(self):
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "Get the current weather in a given location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city and state, e.g. San Francisco, CA",
                            },
                            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                        },
                        "required": ["location"],
                    },
                }
            }
        ]
        messages = [{"role": "user", "content": "What's the weather like in Boston today?"}]
        tool_choice = 'auto'

        tool_choice_response = self.function_call_agent._invoke_with_tools(
            messages=messages, tools=tools, tool_choice=tool_choice
        )

        # ChatCompletion(id='20260224162431488cbd99debc4b99', choices=[
        #     Choice(finish_reason='tool_calls', index=0, logprobs=None,
        #            message=ChatCompletionMessage(content="I'll check the current weather in Boston for you.",
        #                                          refusal=None, role='assistant', annotations=None, audio=None,
        #                                          function_call=None, tool_calls=[
        #                    ChatCompletionMessageFunctionToolCall(id='call_-7881238084484852892', function=Function(
        #                        arguments='{"location":"Boston, MA"}', name='get_current_weather'), type='function',
        #                                                          index=0)],
        #                                          reasoning_content="The user is asking for the weather in Boston today. I need to use the get_current_weather function with Boston as the location. The function requires a location parameter (city and state), and Boston, MA would be appropriate. The unit parameter is optional, so I won't specify it and will let the function use its default."))],
        #                created=1771921492, model='glm-4.7-flash', object='chat.completion', service_tier=None,
        #                system_fingerprint=None,
        #                usage=CompletionUsage(completion_tokens=92, prompt_tokens=202, total_tokens=294,
        #                                      completion_tokens_details=None,
        #                                      prompt_tokens_details=PromptTokensDetails(audio_tokens=None,
        #                                                                                cached_tokens=43)),
        #                request_id='20260224162431488cbd99debc4b99')

        print(tool_choice_response)
