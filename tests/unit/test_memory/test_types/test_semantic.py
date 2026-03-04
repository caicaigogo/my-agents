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
            memory_type='semantic',
            user_id='default_user',
            timestamp=datetime.now(),
            importance=importance,
            metadata=metadata or {}
        )

        # WARNING:hello_agents.memory.types.semantic:🏥 数据库健康状态: Qdrant=✅, Neo4j=✅
        # WARNING:hello_agents.memory.types.semantic:✅ 加载中文spaCy模型: zh_core_web_sm
        # WARNING:hello_agents.memory.types.semantic:✅ 加载英文spaCy模型: en_core_web_sm
        # WARNING:hello_agents.memory.types.semantic:🎯 主要使用中文spaCy模型
        # WARNING:hello_agents.memory.types.semantic:📚 可用语言模型: 中文, 英文
        # WARNING:hello_agents.memory.types.semantic:增强语义记忆初始化完成（使用Qdrant+Neo4j专业数据库）
        # start add
        # WARNING:hello_agents.memory.types.semantic:🌐 检测语言: zh, 使用模型: core_web_sm
        # WARNING:hello_agents.memory.types.semantic:📝 spaCy处理文本: '今天天气很好,我想去上海看看' -> 2 个实体
        # WARNING:hello_agents.memory.storage.neo4j_store:✅ 添加实体: 今天 (TOKEN)
        # WARNING:hello_agents.memory.storage.neo4j_store:✅ 添加实体: 今天 (CONCEPT)
        # WARNING:hello_agents.memory.storage.neo4j_store:✅ 添加关系: token_-4442007345056316253 -REPRESENTS-> concept_-5171279869618731133
        # WARNING:hello_agents.memory.storage.neo4j_store:✅ 添加实体: 天气 (TOKEN)
        # WARNING:hello_agents.memory.storage.neo4j_store:✅ 添加实体: 天气 (CONCEPT)
        # WARNING:hello_agents.memory.storage.neo4j_store:✅ 添加关系: token_5061270527101632259 -REPRESENTS-> concept_-4390717599487003806
        # WARNING:hello_agents.memory.storage.neo4j_store:✅ 添加实体: 很 (TOKEN)
        # WARNING:hello_agents.memory.storage.neo4j_store:✅ 添加实体: 好 (TOKEN)
        # WARNING:hello_agents.memory.storage.neo4j_store:✅ 添加实体: 我 (TOKEN)
        # WARNING:hello_agents.memory.storage.neo4j_store:✅ 添加实体: 想 (TOKEN)
        # WARNING:hello_agents.memory.storage.neo4j_store:✅ 添加实体: 去 (TOKEN)
        # WARNING:hello_agents.memory.storage.neo4j_store:✅ 添加实体: 上海 (TOKEN)
        # WARNING:hello_agents.memory.storage.neo4j_store:✅ 添加实体: 上海 (CONCEPT)
        # WARNING:hello_agents.memory.storage.neo4j_store:✅ 添加关系: token_-4407006926467418749 -REPRESENTS-> concept_1134344460723206021
        # WARNING:hello_agents.memory.storage.neo4j_store:✅ 添加实体: 看看 (TOKEN)
        # WARNING:hello_agents.memory.storage.neo4j_store:✅ 添加关系: token_-4442007345056316253 -NMOD_TMOD-> token_-5695459962904211886
        # WARNING:hello_agents.memory.storage.neo4j_store:✅ 添加关系: token_5061270527101632259 -NSUBJ-> token_-5695459962904211886
        # WARNING:hello_agents.memory.storage.neo4j_store:✅ 添加关系: token_-6675265587455053512 -ADVMOD-> token_-5695459962904211886
        # WARNING:hello_agents.memory.storage.neo4j_store:✅ 添加关系: token_-455069040193920986 -NSUBJ-> token_310403411663914246
        # WARNING:hello_agents.memory.storage.neo4j_store:✅ 添加关系: token_310403411663914246 -CONJ-> token_-5695459962904211886
        # WARNING:hello_agents.memory.storage.neo4j_store:✅ 添加关系: token_-5450888774104072394 -CCOMP-> token_310403411663914246
        # WARNING:hello_agents.memory.storage.neo4j_store:✅ 添加关系: token_-4407006926467418749 -DOBJ-> token_-5450888774104072394
        # WARNING:hello_agents.memory.storage.neo4j_store:✅ 添加关系: token_7809260927148240018 -CONJ-> token_-5450888774104072394
        # WARNING:hello_agents.memory.types.semantic:🔗 已将词法分析结果存储到Neo4j: 9 个词元
        # WARNING:hello_agents.memory.types.semantic:🏷️ spaCy识别实体: '今天' -> DATE (置信度: N/A)
        # WARNING:hello_agents.memory.types.semantic:🏷️ spaCy识别实体: '上海' -> GPE (置信度: N/A)
        # WARNING:hello_agents.memory.storage.neo4j_store:✅ 添加实体: 今天 (DATE)
        # WARNING:hello_agents.memory.storage.neo4j_store:✅ 添加实体: 上海 (GPE)
        # WARNING:hello_agents.memory.storage.neo4j_store:✅ 添加关系: entity_-5171279869618731133 -CO_OCCURS-> entity_1134344460723206021
        # WARNING:hello_agents.memory.storage.qdrant_store:[Qdrant] add_vectors start: n_vectors=1 n_meta=1 collection=hello_agents_vectors
        # WARNING:hello_agents.memory.storage.qdrant_store:[Qdrant] upsert begin: points=1
        # INFO:httpx:HTTP Request: PUT http://localhost:6333/collections/hello_agents_vectors/points?wait=true "HTTP/1.1 200 OK"
        # WARNING:hello_agents.memory.storage.qdrant_store:[Qdrant] upsert done
        # WARNING:hello_agents.memory.storage.qdrant_store:✅ 成功添加 1 个向量到Qdrant
        # WARNING:hello_agents.memory.types.semantic:✅ 添加语义记忆: 2个实体, 1个关系
        memory_item_id = self.memory.add(memory_item)
        print(memory_item_id)


    def test_retrieve(self):
        importance = 0.2
        content = '今天 天气 不错, 去 上海 不知道 怎么样'

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
            memory_type='semantic',
            user_id='default_user',
            timestamp=datetime.now(),
            importance=importance,
            metadata=metadata or {}
        )

        self.memory.add(memory_item)

        query = '今天 天气 很好 , 我 想 去 上海 看看'
        retrieve_results = self.memory.retrieve(query)
        #
        # [MemoryItem(id='fce5cf7f-7b15-4166-abd5-affb01adb385', content='今天 天气 很好', memory_type='episodic',
        #             user_id='default_user', timestamp=datetime.datetime(2026, 2, 26, 13, 42, 3, 700824), importance=0.2,
        #             metadata={'session_id': 'session_20260226_134203', 'context': {}, 'outcome': None,
        #                       'relevance_score': 0.5280000000000001})]
        print(retrieve_results)
