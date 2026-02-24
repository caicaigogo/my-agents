import unittest
from dotenv import load_dotenv
from app.services.llm_service import get_llm
from hello_agents.agents import ReActAgent
from hello_agents.tools import SearchTool, CalculatorTool


class TestReActAgent(unittest.TestCase):

    def setUp(self):

        load_dotenv()
        self.llm = get_llm()
        self.react_agent = ReActAgent(name='react demo', llm=self.llm)

        calculator_tool = CalculatorTool()
        search_tool = SearchTool(backend='tavily')

        self.react_agent.add_tool(calculator_tool)
        self.react_agent.add_tool(search_tool)

    def test_default_prompt(self):
        from hello_agents.agents.react_agent import DEFAULT_REACT_PROMPT
        print(DEFAULT_REACT_PROMPT)

    def test_filled_prompt(self):

        # - python_calculator: 执行数学计算。支持基本运算、数学函数等。例如：2+3*4, sqrt(16), sin(pi/2)等。
        # - search: 智能网页搜索引擎，支持 Tavily后端，可返回结构化或文本化的搜索结果。
        tools_desc = self.react_agent.tool_registry.get_tools_description()

        input_text = '现在买苹果全家桶总的价格是多少'
        history_str = "\n".join(self.react_agent.current_history)
        prompt = self.react_agent.prompt_template.format(
            tools=tools_desc,
            question=input_text,
            history=history_str
        )

        # 你是一个具备推理和行动能力的AI助手。你可以通过思考分析问题，然后调用合适的工具来获取信息，最终给出准确的答案。
        #
        # ## 可用工具
        # - python_calculator: 执行数学计算。支持基本运算、数学函数等。例如：2+3*4, sqrt(16), sin(pi/2)等。
        # - search: 智能网页搜索引擎，支持 Tavily后端，可返回结构化或文本化的搜索结果。
        #
        # ## 工作流程
        # 请严格按照以下格式进行回应，每次只能执行一个步骤：
        #
        # Thought: 分析问题，确定需要什么信息，制定研究策略。
        # Action: 选择合适的工具获取信息，格式为：
        # - `{tool_name}[{tool_input}]`：调用工具获取信息。
        # - `Finish[研究结论]`：当你有足够信息得出结论时。
        #
        # ## 重要提醒
        # 1. 每次回应必须包含Thought和Action两部分
        # 2. 工具调用的格式必须严格遵循：工具名[参数]
        # 3. 只有当你确信有足够信息回答问题时，才使用Finish
        # 4. 如果工具返回的信息不够，继续使用其他工具或相同工具的不同参数
        #
        # ## 当前任务
        # **Question:** 现在买苹果全家桶总的价格是多少
        #
        # ## 执行历史
        #
        #
        # 现在开始你的推理和行动：
        print(prompt)

    def test_parse_react_llm_output(self):

        react_llm_response = """Thought: 用户询问的是现在购买 Apple "全家桶"（通常指 iPhone、MacBook、iPad、Apple Watch 和 AirPods）的总价格。为了给出准确的答案，我需要搜索这些产品在当前时间点的最新价格信息。

Action: search[Apple 全家桶 价格 2024]"""
        print(react_llm_response)

        thought, action = self.react_agent._parse_output(react_llm_response)
        # 用户询问的是现在购买 Apple "全家桶"（通常指 iPhone、MacBook、iPad、Apple Watch 和 AirPods）的总价格。为了给出准确的答案，我需要搜索这些产品在当前时间点的最新价格信息。
        # search[Apple 全家桶 价格 2024]
        print(thought)
        print(action)

    def test_parse_action(self):
        action = """search[Apple 全家桶 价格 2024]"""

        tool_name, tool_input = self.react_agent._parse_action(action)
        # search
        print(tool_name)
        # search[Apple 全家桶 价格 2024]
        print(tool_input)

    def test_agent_run(self):

        input_text = '现在买3辆特斯拉 Model3价格多少'

        # Thought: 用户询问购买3辆特斯拉Model3的当前价格。我需要搜索最新的特斯拉Model3价格信息，特别是中国市场的官方指导价，以计算总价。
        # Observation： 无效的Action格式，请检查。
        # Thought: 用户询问购买3辆特斯拉 Model 3 的当前价格。我需要先搜索 Model 3 的最新价格信息，因为汽车价格会随地区、配置和促销活动变化，需要获取实时的售价数据。
        # Action: search[Tesla Model 3 price]
        # Observation： 搜索关键词：Tesla Model 3 price ...
        # Thought:我已经从搜索结果中获得了特斯拉Model 3的价格信息。根据搜索结果，Model 3起售价为$38,630（来源2和3）。为了计算3辆车的总价格，我需要使用计算器工具进行乘法运算。
        # Action: python_calculator[38630 * 3]
        # Observation： 115890
        # Thought: 搜索结果显示了 Model 3 的不同价格，基础款（标准 Rear-Wheel Drive）起售价为 $38,630。为了给出准确的答案，我需要基于基础价格计算3辆车的总成本，同时说明价格会因配置不同而变化。
        # Action: Finish[特斯拉 Model 3 的价格因配置不同而有所差异。根据搜索结果，标准 Rear-Wheel Drive 起售价为 $38,630。按此价格计算，购买 3 辆车的总成本约为 $115,890。此外，更高配置的车型价格更高，例如 Premium Rear-Wheel Drive 起售价为 $44,130，Performance 起售价为 $56,380。价格通常包含目的地和订单费，但不包含税收和其他费用。]


        # 特斯拉 Model 3 的价格因配置不同而有所差异。根据搜索结果，标准 Rear-Wheel Drive 起售价为 $38,630。按此价格计算，购买 3 辆车的总成本约为 $115,890。此外，更高配置的车型价格更高，例如 Premium Rear-Wheel Drive 起售价为 $44,130，Performance 起售价为 $56,380。价格通常包含目的地和订单费，但不包含税收和其他费用。
        final_answer = self.react_agent.run(input_text=input_text)
        print(final_answer)

        # self.react_agent.current_history
        # ['Observation: 无效的Action格式，请检查。', 'Action: search[Tesla Model 3 price]', "Observation: 🔍 搜索关键词：Tesla Model 3 price\n🧭 使用搜索源：tavily\n\n📚 参考来源：\n[1] 2026 Tesla Model 3 Price, Reviews, Pictures & More\n    The 2026 Tesla Model 3 has a starting sticker price of $38,380, with the range-topping Model 3 Performance kicking off at $56,380. MSRP. KBB Fair Purchase\n    来源: https://www.kbb.com/tesla/model-3/\n\n[2] Model 3 – Sports Electric Sedan | Tesla\n    Model 3 starts at $38,630. Price includes Destination and Order Fees but excludes taxes and other fees. Subject to change. ... Full Self-Driving (Supervised)\n    来源: https://www.tesla.com/model3\n\n[3] Compare | Tesla\n    Model 3 Rear-Wheel Drive starts at $38,630, Model 3 Premium Rear-Wheel Drive starts at $44,130, Model 3 Premium All-Wheel Drive starts at $49,130, Model 3\n    来源: https://www.tesla.com/compare\n\n[4] I Tested the New $36,900 Tesla Model 3 Standard - YouTube\n    I Tested the New $36,900 Tesla Model 3 Standard · Comments.\n    来源: https://www.youtube.com/watch?v=K2It9OqwAnM\n\n[5] Tesla Model 3 leads as the most cost-effective car to operate in the US\n    I'll have to look up brand but it was $200-250 a pop at discount tire. There is a spreadsheet around that has ratings. I picked ones that had\n    来源: https://www.reddit.com/r/teslamotors/comments/1ic01mf/tesla_model_3_leads_as_the_most_costeffective_car/\n", 'Action: python_calculator[38630 * 3]', 'Observation: 115890']
        print(self.react_agent.current_history)

        # [Message(content='现在买3辆特斯拉 Model3价格多少', role='user', timestamp=datetime.datetime(2026, 2, 24, 10, 14, 45, 585092), metadata={}), Message(content='特斯拉 Model 3 的价格因配置不同而有所差异。根据搜索结果，标准 Rear-Wheel Drive 起售价为 $38,630。按此价格计算，购买 3 辆车的总成本约为 $115,890。此外，更高配置的车型价格更高，例如 Premium Rear-Wheel Drive 起售价为 $44,130，Performance 起售价为 $56,380。价格通常包含目的地和订单费，但不包含税收和其他费用。', role='assistant', timestamp=datetime.datetime(2026, 2, 24, 10, 14, 45, 585092), metadata={})]
        print(self.react_agent._history)
