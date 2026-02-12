"""工具基类"""

from abc import ABC, abstractmethod
from typing import Dict, Any



class Tool(ABC):
    """工具基类

    支持两种使用模式：
    1. 普通模式：工具作为单一实体使用
    2. 可展开模式：工具可以展开为多个独立的子工具（每个子工具对应一个功能）

    展开模式支持两种实现方式：
    - 手动定义子工具类（传统方式）
    - 使用 @tool_action 装饰器自动生成（推荐）
    """

    def __init__(self, name: str, description: str, expandable: bool = False):
        """初始化工具

        Args:
            name: 工具名称
            description: 工具描述
            expandable: 是否可展开为多个子工具
        """
        self.name = name
        self.description = description
        self.expandable = expandable

    @abstractmethod
    def run(self, parameters: Dict[str, Any]) -> str:
        """执行工具"""
        pass
