import unittest
from hello_agents.memory import MemoryConfig, WorkingMemory, MemoryItem
import uuid
from datetime import datetime


class TestWorkingMemory(unittest.TestCase):

    def setUp(self):
        self.config = MemoryConfig()
        self.memory = WorkingMemory(self.config)

    def test_add(self):

        importance = 0.2
        content = '这东西不重要'

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

        self.memory.add(memory_item)

        importance = 0.5

        content = '用户刚才问了关于Python函数的问题'

        metadata = {}

        current_session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        # 添加会话信息到元数据
        metadata.update({
            "session_id": current_session_id,
            "timestamp": datetime.now().isoformat()
        })

        # 创建记忆项
        memory_item = MemoryItem(
            id=str(uuid.uuid4()),
            content=content,
            memory_type='working',
            user_id='default_user',
            timestamp=datetime.now(),
            importance=importance,
            metadata=metadata or {}
        )

        self.memory.add(memory_item)
        #
        # [MemoryItem(id='c1a265ea-bcf9-4624-b753-0e6395c09c5c', content='这东西不重要', memory_type='working',
        #             user_id='default_user', timestamp=datetime.datetime(2026, 2, 25, 14, 6, 58, 304328), importance=0.2,
        #             metadata={'session_id': 'session_20260225_140658', 'timestamp': '2026-02-25T14:06:58.304328'}),
        #  MemoryItem(id='c0e9f4b4-cd40-4938-841a-0c706ef9d09c', content='用户刚才问了关于Python函数的问题', memory_type='working',
        #             user_id='default_user', timestamp=datetime.datetime(2026, 2, 25, 14, 6, 58, 305320), importance=0.5,
        #             metadata={'session_id': 'session_20260225_140658', 'timestamp': '2026-02-25T14:06:58.304328'})]
        # [(-0.5, datetime.datetime(2026, 2, 25, 14, 6, 58, 305320),
        #   MemoryItem(id='c0e9f4b4-cd40-4938-841a-0c706ef9d09c', content='用户刚才问了关于Python函数的问题', memory_type='working',
        #              user_id='default_user', timestamp=datetime.datetime(2026, 2, 25, 14, 6, 58, 305320),
        #              importance=0.5,
        #              metadata={'session_id': 'session_20260225_140658', 'timestamp': '2026-02-25T14:06:58.304328'})), (
        #  -0.2, datetime.datetime(2026, 2, 25, 14, 6, 58, 304328),
        #  MemoryItem(id='c1a265ea-bcf9-4624-b753-0e6395c09c5c', content='这东西不重要', memory_type='working',
        #             user_id='default_user', timestamp=datetime.datetime(2026, 2, 25, 14, 6, 58, 304328), importance=0.2,
        #             metadata={'session_id': 'session_20260225_140658', 'timestamp': '2026-02-25T14:06:58.304328'}))]
        print(self.memory.memories)
        print(self.memory.memory_heap)
