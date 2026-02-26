import unittest
from hello_agents.memory import MemoryConfig, EpisodicMemory, MemoryItem
import uuid
from datetime import datetime


class TestEpisodicMemory(unittest.TestCase):

    def setUp(self):
        self.config = MemoryConfig()
        self.memory = EpisodicMemory(self.config)

    def test_add(self):

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
            memory_type='episodic',
            user_id='default_user',
            timestamp=datetime.now(),
            importance=importance,
            metadata=metadata or {}
        )

        memory_item_id = self.memory.add(memory_item)
        print(memory_item_id)

    def test_retrieve(self):
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
            memory_type='episodic',
            user_id='default_user',
            timestamp=datetime.now(),
            importance=importance,
            metadata=metadata or {}
        )

        self.memory.add(memory_item)

        query = '天气'
        retrieve_results = self.memory.retrieve(query)
        #
        # [MemoryItem(id='fce5cf7f-7b15-4166-abd5-affb01adb385', content='今天 天气 很好', memory_type='episodic',
        #             user_id='default_user', timestamp=datetime.datetime(2026, 2, 26, 13, 42, 3, 700824), importance=0.2,
        #             metadata={'session_id': 'session_20260226_134203', 'context': {}, 'outcome': None,
        #                       'relevance_score': 0.5280000000000001})]
        print(retrieve_results)

    def test_get_stats(self):

        stats = self.memory.get_stats()

        # {'count': 0, 'forgotten_count': 0, 'total_count': 0, 'sessions_count': 0, 'avg_importance': 0.0,
        #  'time_span_days': 0.0, 'memory_type': 'episodic',
        #  'document_store': {'users_count': 1, 'memories_count': 8, 'concepts_count': 0, 'memory_concepts_count': 0,
        #                     'concept_relationships_count': 0, 'store_type': 'sqlite',
        #                     'db_path': './memory_data\\memory.db'}}
        print(stats)
