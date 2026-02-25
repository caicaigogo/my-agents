"""记忆工具

为HelloAgents框架提供记忆能力的工具实现。
可以作为工具添加到任何Agent中，让Agent具备记忆功能。
"""

from typing import Dict, Any, List
from datetime import datetime

from ..base import Tool, ToolParameter, tool_action

from ...memory import MemoryManager, MemoryConfig


class MemoryTool(Tool):
    """记忆工具

    为Agent提供记忆功能：
    - 添加记忆
    - 检索相关记忆
    - 获取记忆摘要
    - 管理记忆生命周期
    """

    def __init__(
        self,
        user_id: str = "default_user",
        memory_config: MemoryConfig = None,
        memory_types: List[str] = None,
        expandable: bool = False
    ):
        super().__init__(
            name="memory",
            description="记忆工具 - 可以存储和检索对话历史、知识和经验",
            expandable=expandable
        )

        # 初始化记忆管理器
        self.memory_config = memory_config or MemoryConfig()
        self.memory_types = memory_types or ["working", "episodic", "semantic"]

        self.memory_manager = MemoryManager(
            config=self.memory_config,
            user_id=user_id,
            enable_working="working" in self.memory_types,
            enable_episodic="episodic" in self.memory_types,
            enable_semantic="semantic" in self.memory_types,
            enable_perceptual="perceptual" in self.memory_types
        )

        # 会话状态
        self.current_session_id = None
        self.conversation_count = 0

    def run(self, parameters: Dict[str, Any]) -> str:
        """执行工具（非展开模式）

        Args:
            parameters: 工具参数字典，必须包含action参数

        Returns:
            执行结果字符串
        """
        if not self.validate_parameters(parameters):
            return "❌ 参数验证失败：缺少必需的参数"

        action = parameters.get("action")

        # 根据action调用对应的方法，传入提取的参数
        if action == "add":
            return self._add_memory(
                content=parameters.get("content", ""),
                memory_type=parameters.get("memory_type", "working"),
                importance=parameters.get("importance", 0.5),
                file_path=parameters.get("file_path"),
                modality=parameters.get("modality")
            )

    @tool_action("memory_add", "添加新记忆到记忆系统中")
    def _add_memory(
        self,
        content: str = "",
        memory_type: str = "working",
        importance: float = 0.5,
        file_path: str = None,
        modality: str = None
    ) -> str:
        """添加记忆

        Args:
            content: 记忆内容
            memory_type: 记忆类型：working(工作记忆), episodic(情景记忆), semantic(语义记忆), perceptual(感知记忆)
            importance: 重要性分数，0.0-1.0
            file_path: 感知记忆：本地文件路径（image/audio）
            modality: 感知记忆模态：text/image/audio（不传则按扩展名推断）

        Returns:
            执行结果
        """
        metadata = {}
        try:
            # 确保会话ID存在
            if self.current_session_id is None:
                self.current_session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


            # 添加会话信息到元数据
            metadata.update({
                "session_id": self.current_session_id,
                "timestamp": datetime.now().isoformat()
            })

            memory_id = self.memory_manager.add_memory(
                content=content,
                memory_type=memory_type,
                importance=importance,
                metadata=metadata,
                auto_classify=False  # 禁用自动分类，使用明确指定的类型
            )

            return f"✅ 记忆已添加 (ID: {memory_id[:8]}...)"

        except Exception as e:
            return f"❌ 添加记忆失败: {str(e)}"
