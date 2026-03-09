"""
Benchmarks 模块

包含各种智能体评估基准测试:
- BFCL: Berkeley Function Calling Leaderboard
- GAIA: General AI Assistants Benchmark
- Data Generation: 数据生成质量评估
"""

from hello_agents.evaluation.benchmarks.bfcl.evaluator import BFCLEvaluator
from hello_agents.evaluation.benchmarks.gaia.evaluator import GAIAEvaluator

__all__ = [
    "BFCLEvaluator",
    "GAIAEvaluator",
]

