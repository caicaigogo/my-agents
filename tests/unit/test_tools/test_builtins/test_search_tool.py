import unittest
import json
from dotenv import load_dotenv

from hello_agents.tools import SearchTool
from app.services.llm_service import get_llm
from hello_agents.agents import SimpleAgent
from hello_agents.tools import ToolRegistry


class TestCalculatorTool(unittest.TestCase):

    def setUp(self):

        load_dotenv()

    def test_tool_run(self):

        search_tool = SearchTool()
        parameters = {
            'input': '特斯拉有几款车型',
            'backend': 'tavily',
            'fetch_full_page': True,
            'mode': 'text'

        }
        text_result = search_tool.run(parameters)
        print('text result \n', text_result)

        parameters = {
            'input': '特斯拉有几款车型',
            'backend': 'tavily',
            'fetch_full_page': True,
            'mode': 'structured'
        }
        structured_result = search_tool.run(parameters)
        print(json.dumps(structured_result, ensure_ascii=False))


    def test_tool_invoke(self):

        search_tool = SearchTool(backend='tavily')
        tool_registry = ToolRegistry()
        tool_registry.register_tool(search_tool)

        system_prompt = '你是能使用tools的人工智能agent'

        llm = get_llm()
        tool_invoke_agent = SimpleAgent(
            name="search agent demo",
            llm=llm,
            system_prompt=system_prompt,
            tool_registry=tool_registry,
            enable_tool_calling=True
        )

        user_query = '特斯拉有几款车型'
        # glm-4-flash: python_calculator\n5+3
        # 指令跟随能力不强

        # glm-4.7-flash -> `[TOOL_CALL:python_calculator:expression=5+3]`
        # glm-4.7-flash, 指令跟随能力有进步，但是多了参数名 expression

        tool_invoke_agent.run(user_query)
        # [{'role': 'system', 'content': '你是能使用tools的人工智能agent\n\n## 可用工具\n你可以使用以下工具来帮助回答问题：\n- search: 智能网页搜索引擎，支持 Tavily后端，可返回结构化或文本化的搜索结果。\n\n## 工具调用格式\n当需要使用工具时，请使用以下格式：\n`[TOOL_CALL:{tool_name}:{parameters}]`\n\n### 参数格式说明\n1. **多个参数**：使用 `key=value` 格式，用逗号分隔\n   示例：`[TOOL_CALL:calculator_multiply:a=12,b=8]`\n   示例：`[TOOL_CALL:filesystem_read_file:path=README.md]`\n\n2. **单个参数**：直接使用 `key=value`\n   示例：`[TOOL_CALL:search:query=Python编程]`\n\n3. **简单查询**：可以直接传入文本\n   示例：`[TOOL_CALL:search:Python编程]`\n\n### 重要提示\n- 参数名必须与工具定义的参数名完全匹配\n- 数字参数直接写数字，不需要引号：`a=12` 而不是 `a="12"`\n- 文件路径等字符串参数直接写：`path=README.md`\n- 工具调用结果会自动插入到对话中，然后你可以基于结果继续回答\n'}, {'role': 'user', 'content': '特斯拉有几款车型'}]
        # `[TOOL_CALL:search:query=特斯拉2024年最新车型列表 Model S Model X Model 3 Model Y Cybertruck]`
        # [{'role': 'system', 'content': '你是能使用tools的人工智能agent\n\n## 可用工具\n你可以使用以下工具来帮助回答问题：\n- search: 智能网页搜索引擎，支持 Tavily后端，可返回结构化或文本化的搜索结果。\n\n## 工具调用格式\n当需要使用工具时，请使用以下格式：\n`[TOOL_CALL:{tool_name}:{parameters}]`\n\n### 参数格式说明\n1. **多个参数**：使用 `key=value` 格式，用逗号分隔\n   示例：`[TOOL_CALL:calculator_multiply:a=12,b=8]`\n   示例：`[TOOL_CALL:filesystem_read_file:path=README.md]`\n\n2. **单个参数**：直接使用 `key=value`\n   示例：`[TOOL_CALL:search:query=Python编程]`\n\n3. **简单查询**：可以直接传入文本\n   示例：`[TOOL_CALL:search:Python编程]`\n\n### 重要提示\n- 参数名必须与工具定义的参数名完全匹配\n- 数字参数直接写数字，不需要引号：`a=12` 而不是 `a="12"`\n- 文件路径等字符串参数直接写：`path=README.md`\n- 工具调用结果会自动插入到对话中，然后你可以基于结果继续回答\n'}, {'role': 'user', 'content': '特斯拉有几款车型'}, {'role': 'assistant', 'content': '``'}, {'role': 'user', 'content': '工具执行结果：\n🔧 工具 search 执行结果：\n🔍 搜索关键词：特斯拉2024年最新车型列表 Model S Model X Model 3 Model Y Cybertruck\n🧭 使用搜索源：tavily\n\n📚 参考来源：\n[1] 2024 Tesla SUVs and Trucks: What\'s New With Model X, Y, ...\n    # 2024 Tesla SUVs and Trucks: What’s New With Model X, Y, and Cybertruck. Amid its outrageous performance models and colossal semi-trucks, Tesla hasn\'t forgotten about its first SUV, the Model X, which also receives a few notable updates. ### **2024 Tesla Model Y: What\'s New**. The Model Y is Tesla\'s bestseller, and it\'s among the bestselling vehicles in the world right now, so any significant update to the electric SUV that debuted on the road in 2020 is a big deal. ### **2024 Tesla Model Y: What\'s New**. If Tesla makes these changes and transforms the Model Y the way it did the Model 3 Highland, we\'re in for a treat. ### **2024 Tesla Model Y Pros and Cons**. ### **2024 Tesla Model X: What\'s New**. ### **2024 Tesla Model X Pros and Cons**. * 2024 Tesla Model Y: Significant update (anticipated). * 2024 Tesla Model X: Minor update. * 2024 Tesla Cybertruck: All-new model.\n    来源: https://www.motortrend.com/features/2024-tesla-suvs-truck-lineup-updates-changes\n\n[2] New 2024 Models Are HERE! | Tesla Model 3 + Model Y - YouTube\n    ... s/emQo Tesla\'s all-new 2024 lineup is here with major upgrades for the Model 3, Model Y, Model S, Model X, and Cybertruck! Plus I\'ve got an\n    来源: https://www.youtube.com/watch?v=-zuMFEbgrWc\n\n[3] Tesla 2024 Model List: Current Lineup - Tesery\n    ### 2024 Tesla Model Y Long Range: The All-Rounder. Transform Your Tesla: Tesery Model 3/Y Dashboard & Door Trim Review. TESERY 19" /20" Wheel Brake Caliper Cover For Tesla Model Y 2020-2026. Product Specifications Compatibility: Tesla Model Y Juniper 2025 - Present Material: 100% Genuine Carbon Fiber... Tesla Model Y Juniper ABS Front Lip Spoiler (2025+) Transform the front end of your... LED Logo Tesla Puddle Lights for Model 3/Y/S/X | TESERY. LED Logo Tesla Puddle Lights for Model 3 Highland / Y / S / X... For Tesla Model 3 (2017–2023) & Model Y (2020–2025.03) Tesla Rear Entertainment System Screen Display... TESERY Roof Rack for Tesla Model 3 Highland / Model Y (Set of 2). Mud Flaps Splash Guards for Tesla Model 3 / Y. TESERY Logo Cover Front Badge Rear Letters Emblem for Tesla Model 3 / Y - Real Carbon Fiber Exterior. TESERY Smart Ring Key for Tesla Model 3 / Y / S / X / Cybertruck.\n    来源: https://www.tesery.com/blogs/news/tesla-2024-model-list-current-lineup\n\n[4] Model 3, Model S, Model X, Model Y, Cybertruck, and ...\n    ## Tesla Model 3. It’s Tesla’s most affordable model, and it offers rear-wheel or all-wheel drive (AWD). From launch, all versions came very well-equipped but in October 2025 Tesla introduced a new entry-level ‘Standard’ model. As of this writing, if you’re buying a new model you can currently choose from four variants: Standard Rear-Wheel Drive, Premium Rear-Wheel Drive (formerly known as Long-Range All-Wheel Drive), Premium All-Wheel Drive, and the Performance All-Wheel Drive. A starting price of $38,630 (including destination fee) makes the Model 3 Standard Rear-Wheel Drive very competitively priced. ## Tesla Model S. Prices for the All-Wheel Drive model start at $96,630 (including destination fee and order fee), the Plaid variant coming in at $116,130. ## Tesla Model X. ## Tesla Model Y. An all-new Roadster prototype was unveiled in late 2017, with Tesla reporting that it would have a 0-60mph time of less than two seconds, more than 600 miles of range and a starting price of about $200,000. On top of excellent battery range and distinctive design, each of Tesla’s models offers the following benefits:.\n    来源: https://www.cargurus.com/Cars/articles/tesla-models-compared\n\n[5] Model S vs. Cybertruck vs. Model Y vs. Model 3 vs. Model X - YouTube\n    I finally drove the Tesla Cybertruck and it blew me away. · Cybertruck vs Model X: Cabin Noise, Steering and Kid Tested · Perfect Tesla setup:\n    来源: https://www.youtube.com/watch?v=e3fDUID7LvE\n\n\n请基于这些结果给出完整的回答。'}]
        # [Message(content='特斯拉有几款车型', role='user', timestamp=datetime.datetime(2026, 2, 13, 11, 12, 3, 331260), metadata={}), Message(content='根据搜索结果，特斯拉目前主要有以下**5款车型**：\n\n## 🚗 特斯拉主要车型列表\n\n### 1. **Model 3** - 中端轿车\n- 特斯拉最经济实惠的车型\n- 起售价约 $38,630（含运费）\n- 提供多种配置：标准后轮驱动版、后轮驱动增强版、全轮驱动版、高性能全轮驱动版\n- 2024年进行了重大升级（被称为"Highland"改款）\n\n### 2. **Model Y** - 中端SUV\n- 特斯拉销量最好的车型，也是全球最畅销的汽车之一\n- 2024年预计会有显著更新\n- 2025年即将推出新款"Juniper"版本\n\n### 3. **Model S** - 高端轿车\n- 起售价约 $96,630（全轮驱动版）\n- Plaid版本售价约 $116,130\n- 高性能豪华轿车\n\n### 4. **Model X** - 高端SUV\n- 特斯拉首款SUV车型\n- 2024年进行了小幅更新\n- 以鹰翼门设计和高端定位著称\n\n### 5. **Cybertruck** - 电动皮卡\n- 全新车型，于2019年首次亮相\n- 预计2024年推出\n- 独特的未来感设计\n\n## 📊 总结\n特斯拉目前的产品线覆盖了**轿车、SUV和皮卡**三大类别，从经济实惠的Model 3到豪华的Model S/X，再到全新的Cybertruck，形成了完整的产品矩阵。2024年，特斯拉对所有主要车型都进行了不同程度的更新升级。', role='assistant', timestamp=datetime.datetime(2026, 2, 13, 11, 12, 3, 331260), metadata={})]
        print(tool_invoke_agent.get_history())
