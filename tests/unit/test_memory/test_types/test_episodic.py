import unittest
from hello_agents.memory import MemoryConfig, EpisodicMemory, MemoryItem
import uuid
from datetime import datetime


class TestEpisodicMemory(unittest.TestCase):

    def setUp(self):
        self.config = MemoryConfig()

    def test_add(self):

        self.memory = EpisodicMemory(self.config)

        importance = 0.2
        content = '今天 天气 很好'

        metadata = {}

        current_session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        # 添加会话信息到元数据
        metadata.update({
            "session_id": current_session_id,
            "timestamp": datetime.now().isoformat()
        })

        memory_item = MemoryItem(
            id=str(uuid.uuid4()),
            content=content,
            memory_type='working',
            user_id='default_user',
            timestamp=datetime.now(),
            importance=importance,
            metadata=metadata or {}
        )

        memory_item_id = self.memory.add(memory_item)
        print(memory_item_id)
