import unittest
from dotenv import load_dotenv
from app.services.llm_service import get_llm
from hello_agents.agents import PlanAndSolveAgent


class TestPlanAndSolveAgent(unittest.TestCase):

    def setUp(self):

        load_dotenv()
        self.llm = get_llm()
        self.plan_and_solve_agent = PlanAndSolveAgent(name='plan and solve demo', llm=self.llm)

    def test_default_prompt(self):
        from hello_agents.agents.plan_solve_agent import DEFAULT_PLANNER_PROMPT, DEFAULT_EXECUTOR_PROMPT
        print('DEFAULT_PLANNER_PROMPT')
        print(DEFAULT_PLANNER_PROMPT)
        print('DEFAULT_EXECUTOR_PROMPT')
        print(DEFAULT_EXECUTOR_PROMPT)

    def test_planner_fill_prompt(self):

        planer = self.plan_and_solve_agent.planner
        question = "一个水果店周一卖出了15个苹果。周二卖出的苹果数量是周一的两倍。周三卖出的数量比周二少了5个。请问这三天总共卖出了多少个苹果？"

        planer_fill_prompt = planer.prompt_template.format(question=question)
        # 你是一个顶级的AI规划专家。你的任务是将用户提出的复杂问题分解成一个由多个简单步骤组成的行动计划。
        # 请确保计划中的每个步骤都是一个独立的、可执行的子任务，并且严格按照逻辑顺序排列。
        # 你的输出必须是一个Python列表，其中每个元素都是一个描述子任务的字符串。
        #
        # 问题: 一个水果店周一卖出了15个苹果。周二卖出的苹果数量是周一的两倍。周三卖出的数量比周二少了5个。请问这三天总共卖出了多少个苹果？
        #
        # 请严格按照以下格式输出你的计划:
        # ```python
        # ["步骤1", "步骤2", "步骤3", ...]
        # ```
        print(planer_fill_prompt)

    def test_executor_fill_prompt(self):

        executor = self.plan_and_solve_agent.executor
        history = ""
        plan = ['计算周一卖出的苹果数量', '计算周二卖出的苹果数量（周一数量乘以2）', '计算周三卖出的苹果数量（周二数量减去5）', '计算三天卖出的苹果总数（将周一、周二和周三的数量相加）']
        question = "一个水果店周一卖出了15个苹果。周二卖出的苹果数量是周一的两倍。周三卖出的数量比周二少了5个。请问这三天总共卖出了多少个苹果？"
        # 当前step
        step = '计算周一卖出的苹果数量'
        executor_fill_prompt = executor.prompt_template.format(
            question=question,
            plan=plan,
            history=history if history else "无",
            current_step=step
        )
        #
        # 你是一位顶级的AI执行专家。你的任务是严格按照给定的计划，一步步地解决问题。
        # 你将收到原始问题、完整的计划、以及到目前为止已经完成的步骤和结果。
        # 请你专注于解决
        # "当前步骤"，并仅输出该步骤的最终答案，不要输出任何额外的解释或对话。
        #
        # # 原始问题:
        # 一个水果店周一卖出了15个苹果。周二卖出的苹果数量是周一的两倍。周三卖出的数量比周二少了5个。请问这三天总共卖出了多少个苹果？
        #
        # # 完整计划:
        # ['计算周一卖出的苹果数量', '计算周二卖出的苹果数量（周一数量乘以2）', '计算周三卖出的苹果数量（周二数量减去5）', '计算三天卖出的苹果总数（将周一、周二和周三的数量相加）']
        #
        # # 历史步骤与结果:
        # 无
        #
        # # 当前步骤:
        # 计算周一卖出的苹果数量
        #
        # 请仅输出针对
        # "当前步骤"
        # 的回答:
        print(executor_fill_prompt)

        history = """步骤 1: 计算周一卖出的苹果数量
结果: 15

步骤 2: 计算周二卖出的苹果数量（周一数量乘以2）
结果: 30

步骤 3: 计算周三卖出的苹果数量（周二数量减去5）
结果: 25

"""
        step = '计算三天卖出的苹果总数（将周一、周二和周三的数量相加）'
        executor_fill_prompt = executor.prompt_template.format(
            question=question,
            plan=plan,
            history=history if history else "无",
            current_step=step
        )

        # 你是一位顶级的AI执行专家。你的任务是严格按照给定的计划，一步步地解决问题。
        # 你将收到原始问题、完整的计划、以及到目前为止已经完成的步骤和结果。
        # 请你专注于解决"当前步骤"，并仅输出该步骤的最终答案，不要输出任何额外的解释或对话。

        # # 原始问题:
        # 一个水果店周一卖出了15个苹果。周二卖出的苹果数量是周一的两倍。周三卖出的数量比周二少了5个。请问这三天总共卖出了多少个苹果？

        # # 完整计划:
        # ['计算周一卖出的苹果数量', '计算周二卖出的苹果数量（周一数量乘以2）', '计算周三卖出的苹果数量（周二数量减去5）', '计算三天卖出的苹果总数（将周一、周二和周三的数量相加）']

        # # 历史步骤与结果:
        # 步骤 1: 计算周一卖出的苹果数量
        # 结果: 15

        # 步骤 2: 计算周二卖出的苹果数量（周一数量乘以2）
        # 结果: 30

        # 步骤 3: 计算周三卖出的苹果数量（周二数量减去5）
        # 结果: 25

        # # 当前步骤:
        # 计算三天卖出的苹果总数（将周一、周二和周三的数量相加）

        # 请仅输出针对"当前步骤"的回答:

        print(executor_fill_prompt)

    def test_planner_plan(self):

        planer = self.plan_and_solve_agent.planner
        question = "一个水果店周一卖出了15个苹果。周二卖出的苹果数量是周一的两倍。周三卖出的数量比周二少了5个。请问这三天总共卖出了多少个苹果？"

        # ```python
        # ["计算周一卖出的苹果数量", "计算周二卖出的苹果数量（周一数量乘以2）", "计算周三卖出的苹果数量（周二数量减去5）", "计算三天卖出的苹果总数（将周一、周二和周三的数量相加）"]
        # ```

        # ['计算周一卖出的苹果数量', '计算周二卖出的苹果数量（周一数量乘以2）', '计算周三卖出的苹果数量（周二数量减去5）', '计算三天卖出的苹果总数（将周一、周二和周三的数量相加）']
        plan_list = planer.plan(question)
        print(plan_list)

    def test_executor_execute(self):

        executor = self.plan_and_solve_agent.executor

        plan = ['计算周一卖出的苹果数量', '计算周二卖出的苹果数量（周一数量乘以2）', '计算周三卖出的苹果数量（周二数量减去5）', '计算三天卖出的苹果总数（将周一、周二和周三的数量相加）']
        question = "一个水果店周一卖出了15个苹果。周二卖出的苹果数量是周一的两倍。周三卖出的数量比周二少了5个。请问这三天总共卖出了多少个苹果？"

        # --- 正在执行计划 ---

        # -> 正在执行步骤 1/4: 计算周一卖出的苹果数量
        # ✅ 步骤 1 已完成，结果: 15

        # -> 正在执行步骤 2/4: 计算周二卖出的苹果数量（周一数量乘以2）
        # ✅ 步骤 2 已完成，结果: 30

        # -> 正在执行步骤 3/4: 计算周三卖出的苹果数量（周二数量减去5）
        # ✅ 步骤 3 已完成，结果: 25

        # -> 正在执行步骤 4/4: 计算三天卖出的苹果总数（将周一、周二和周三的数量相加）

        # ✅ 步骤 4 已完成，结果: 70

        final_answer = executor.execute(question=question, plan=plan)

        # 70
        print(final_answer)

        # history

        # 步骤 1: 计算周一卖出的苹果数量
        # 结果: 15

        # 步骤 2: 计算周二卖出的苹果数量（周一数量乘以2）
        # 结果: 30

        # 步骤 3: 计算周三卖出的苹果数量（周二数量减去5）
        # 结果: 25

        # 步骤 4: 计算三天卖出的苹果总数（将周一、周二和周三的数量相加）
        # 结果: 70

    def test_agent_run(self):

        input_text = "一个水果店周一卖出了15个苹果。周二卖出的苹果数量是周一的两倍。周三卖出的数量比周二少了5个。请问这三天总共卖出了多少个苹果？"

        # 🤖 plan and solve demo 开始处理问题: 一个水果店周一卖出了15个苹果。周二卖出的苹果数量是周一的两倍。周三卖出的数量比周二少了5个。请问这三天总共卖出了多少个苹果？
        # --- 正在生成计划 ---
        # ✅ 计划已生成:
        # ```python
        # ["获取周一卖出的苹果数量", "计算周二卖出的苹果数量", "计算周三卖出的苹果数量", "将三天卖出的苹果数量相加"]
        # ```

        # --- 正在执行计划 ---

        # -> 正在执行步骤 1/4: 获取周一卖出的苹果数量
        # ✅ 步骤 1 已完成，结果: 15

        # -> 正在执行步骤 2/4: 计算周二卖出的苹果数量
        # ✅ 步骤 2 已完成，结果: 30

        # -> 正在执行步骤 3/4: 计算周三卖出的苹果数量
        # ✅ 步骤 3 已完成，结果: 25

        # -> 正在执行步骤 4/4: 将三天卖出的苹果数量相加

        # ✅ 步骤 4 已完成，结果: 70

        final_answer = self.plan_and_solve_agent.run(input_text=input_text)

        # 70
        print(final_answer)

        # [Message(content='一个水果店周一卖出了15个苹果。周二卖出的苹果数量是周一的两倍。周三卖出的数量比周二少了5个。请问这三天总共卖出了多少个苹果？', role='user', timestamp=datetime.datetime(2026, 2, 24, 10, 20, 48, 832812), metadata={}), Message(content='70', role='assistant', timestamp=datetime.datetime(2026, 2, 24, 10, 20, 48, 832812), metadata={})]
        print(self.plan_and_solve_agent._history)
