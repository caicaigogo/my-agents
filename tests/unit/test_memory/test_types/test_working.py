import unittest
from hello_agents.memory import MemoryConfig, WorkingMemory, MemoryItem
import uuid
from datetime import datetime


class TestWorkingMemory(unittest.TestCase):

    def setUp(self):
        self.config = MemoryConfig()
        self.memory = WorkingMemory(self.config)

        importance = 0.2
        content = '这 东西 不 重要'

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

        content = '用户 刚才 问 了 关于 Python 函数 的 问题'

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

    def test_add(self):

        # [MemoryItem(id='4282c8c6-9cf2-4ca1-9a2d-a3d172222726', content='这 东西 不 重要', memory_type='working',
        #             user_id='default_user', timestamp=datetime.datetime(2026, 2, 25, 16, 4, 27, 406965), importance=0.2,
        #             metadata={'session_id': 'session_20260225_160427', 'timestamp': '2026-02-25T16:04:27.405968'}),
        #  MemoryItem(id='8c808163-903c-4e45-872a-d570f8bc67c9', content='用户 刚才 问 了 关于 Python 函数 的 问题', memory_type='working',
        #             user_id='default_user', timestamp=datetime.datetime(2026, 2, 25, 16, 4, 27, 406965), importance=0.5,
        #             metadata={'session_id': 'session_20260225_160427', 'timestamp': '2026-02-25T16:04:27.406965'})]
        # [(-0.5, datetime.datetime(2026, 2, 25, 16, 4, 27, 406965),
        #   MemoryItem(id='8c808163-903c-4e45-872a-d570f8bc67c9', content='用户 刚才 问 了 关于 Python 函数 的 问题',
        #              memory_type='working', user_id='default_user',
        #              timestamp=datetime.datetime(2026, 2, 25, 16, 4, 27, 406965), importance=0.5,
        #              metadata={'session_id': 'session_20260225_160427', 'timestamp': '2026-02-25T16:04:27.406965'})), (
        #  -0.2, datetime.datetime(2026, 2, 25, 16, 4, 27, 406965),
        #  MemoryItem(id='4282c8c6-9cf2-4ca1-9a2d-a3d172222726', content='这 东西 不 重要', memory_type='working',
        #             user_id='default_user', timestamp=datetime.datetime(2026, 2, 25, 16, 4, 27, 406965), importance=0.2,
        #             metadata={'session_id': 'session_20260225_160427', 'timestamp': '2026-02-25T16:04:27.405968'}))]
        print(self.memory.memories)
        print(self.memory.memory_heap)

    def test_retrieve(self):

           # vector score
           # {'5108b047-e6f5-4c08-9ff3-120e30111d5b': np.float64(0.816496580927726),
           #  '850aabb8-8cfa-4317-b4f6-04d3b3334c6c': np.float64(0.1859081826077956)}
           # [MemoryItem(id='5108b047-e6f5-4c08-9ff3-120e30111d5b', content='这 东西 不 重要', memory_type='working',
           #             user_id='default_user', timestamp=datetime.datetime(2026, 2, 25, 16, 1, 31, 582641),
           #             importance=0.2,
           #             metadata={'session_id': 'session_20260225_160131', 'timestamp': '2026-02-25T16:01:31.582641'}),
           #  MemoryItem(id='850aabb8-8cfa-4317-b4f6-04d3b3334c6c', content='用户 刚才 问 了 关于 Python 函数 的 问题',
           #             memory_type='working', user_id='default_user',
           #             timestamp=datetime.datetime(2026, 2, 25, 16, 1, 31, 582641), importance=0.5,
           #             metadata={'session_id': 'session_20260225_160131', 'timestamp': '2026-02-25T16:01:31.582641'})]

           query = '函数 这 东西 不 重要'
           retrieve_results = self.memory.retrieve(query)
           print(retrieve_results)
