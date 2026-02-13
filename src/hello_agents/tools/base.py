"""工具基类"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from pydantic import BaseModel

class ToolParameter(BaseModel):
    """工具参数定义"""
    name: str
    type: str
    description: str
    required: bool = True
    default: Any = None


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

    @abstractmethod
    def get_parameters(self) -> List[ToolParameter]:
        """获取工具参数定义"""
        pass

    def __str__(self) -> str:
        return f"Tool(name={self.name})"

    def __repr__(self) -> str:
        return self.__str__()
