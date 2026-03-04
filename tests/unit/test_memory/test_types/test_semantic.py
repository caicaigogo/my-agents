import unittest
from hello_agents.memory import MemoryConfig, SemanticMemory, MemoryItem
import uuid
from datetime import datetime
from dotenv import load_dotenv


class TestSemanticMemory(unittest.TestCase):

    def setUp(self):
        load_dotenv()

        self.config = MemoryConfig()
        self.memory = SemanticMemory(self.config)

    def test_add(self):

        content = '今天天气很好,我想去上海看看'
        importance = 0.5
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
            memory_type='episodic',
            user_id='default_user',
            timestamp=datetime.now(),
            importance=importance,
            metadata=metadata or {}
        )

        print('start add')
        memory_item_id = self.memory.add(memory_item)
        print(memory_item_id)
