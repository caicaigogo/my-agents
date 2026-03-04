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

        # WARNING:hello_agents.memory.types.semantic:🔗 已将词法分析结果存储到Neo4j: 9 个词元
        # WARNING:hello_agents.memory.types.semantic:🏷️ spaCy识别实体: '今天' -> DATE (置信度: N/A)
        # WARNING:hello_agents.memory.types.semantic:🏷️ spaCy识别实体: '上海' -> GPE (置信度: N/A)
        # WARNING:hello_agents.memory.storage.neo4j_store:🔍 找到 1 个相关实体
        # WARNING:hello_agents.memory.storage.neo4j_store:🔍 找到 1 个相关实体
        # WARNING:hello_agents.memory.types.semantic:🔍 查找记忆ID: ead17ece-df0f-4f33-8c7d-ec6956916f4f, 当前记忆数: 1
        # WARNING:hello_agents.memory.types.semantic:✅ 找到记忆: 今天 天气 不错, 去 上海 不知道 怎么样...
        # WARNING:hello_agents.memory.types.semantic:🕸️ Neo4j图搜索返回 1 个结果
        # WARNING:hello_agents.memory.types.semantic:⚠️ 跳过重复内容: 今天 天气 不错, 去 上海 不知道 怎么样...
        # WARNING:hello_agents.memory.types.semantic:🔍 向量结果: 3, 图结果: 1
        # WARNING:hello_agents.memory.types.semantic:📝 去重后: 2, 过滤后: 0
        # WARNING:hello_agents.memory.types.semantic:✅ 检索到 0 条相关记忆


        # WARNING:hello_agents.memory.types.semantic:🏷️ spaCy识别实体: '今天' -> DATE (置信度: N/A)
        # WARNING:hello_agents.memory.types.semantic:🏷️ spaCy识别实体: '上海' -> GPE (置信度: N/A)
        # WARNING:hello_agents.memory.storage.neo4j_store:🔍 找到 1 个相关实体
        # WARNING:hello_agents.memory.storage.neo4j_store:🔍 找到 1 个相关实体
        # WARNING:hello_agents.memory.types.semantic:🔍 查找记忆ID: da22da71-c7d2-4021-ad42-9a2ac9bdd264, 当前记忆数: 1
        # WARNING:hello_agents.memory.types.semantic:✅ 找到记忆: 今天 天气 不错, 去 上海 不知道 怎么样...
        # WARNING:hello_agents.memory.types.semantic:🕸️ Neo4j图搜索返回 1 个结果
        # WARNING:hello_agents.memory.types.semantic:⚠️ 跳过重复内容: 今天 天气 不错, 去 上海 不知道 怎么样...
        # WARNING:hello_agents.memory.types.semantic:⚠️ 跳过重复内容: 今天 天气 不错, 去 上海 不知道 怎么样...
        # WARNING:hello_agents.memory.types.semantic:⚠️ 跳过重复内容: 今天 天气 不错, 去 上海 不知道 怎么样...
        # WARNING:hello_agents.memory.types.semantic:🔍 向量结果: 5, 图结果: 1
        # WARNING:hello_agents.memory.types.semantic:📝 去重后: 2, 过滤后: 2
        # WARNING:hello_agents.memory.types.semantic:  结果1: 向量=0.000, 图=0.600, 精确=0.000, 关键词=0.000, 公司=0.000, 实体=0.000, 综合=0.158
        # WARNING:hello_agents.memory.types.semantic:  结果2: 向量=0.000, 图=0.000, 精确=0.000, 关键词=0.000, 公司=0.000, 实体=0.000, 综合=0.000
        # WARNING:hello_agents.memory.types.semantic:✅ 检索到 2 条相关记忆
        # [MemoryItem(id='da22da71-c7d2-4021-ad42-9a2ac9bdd264', content='今天 天气 不错, 去 上海 不知道 怎么样', memory_type='semantic', user_id='default_user', timestamp=datetime.datetime(2026, 3, 4, 15, 45, 34), importance=0.2, metadata={'combined_score': 0.1584, 'vector_score': 0.0, 'graph_score': 0.6, 'probability': 0.5395174083728296}), MemoryItem(id='ac081f3b-5fa7-450f-922c-6320c11d96ba', content='今天天气很好,我想去上海看看', memory_type='semantic', user_id='default_user', timestamp=datetime.datetime(2026, 3, 4, 15, 25, 22), importance=0.5, metadata={'combined_score': 0.0, 'vector_score': 0.0, 'graph_score': 0.0, 'probability': 0.46048259162717037})]

        print(retrieve_results)

    def test_export_knowledge_graph(self):

        knowledge_graph = self.memory.export_knowledge_graph()

        # {'entities': {}, 'relations': [],
        #  'graph_stats': {'total_nodes': 100, 'entity_nodes': 100, 'memory_nodes': 0, 'total_relationships': 96,
        #                  'cached_entities': 0, 'cached_relations': 0}}
        print(knowledge_graph)
