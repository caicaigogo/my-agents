"""语义记忆实现

结合向量检索和知识图谱的混合语义记忆，使用：
- HuggingFace 中文预训练模型进行文本嵌入
- 向量相似度检索进行快速初筛
- 知识图谱进行实体关系推理
- 混合检索策略优化结果质量
"""

from typing import List, Dict, Any, Optional, Set, Tuple
from datetime import datetime, timedelta
import json
import logging
import math
import numpy as np

from ..base import BaseMemory, MemoryItem, MemoryConfig
from ..embedding import get_text_embedder, get_dimension


# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Entity:
    """实体类"""

    def __init__(
        self,
        entity_id: str,
        name: str,
        entity_type: str = "MISC",
        description: str = "",
        properties: Dict[str, Any] = None
    ):
        self.entity_id = entity_id
        self.name = name
        self.entity_type = entity_type  # PERSON, ORG, PRODUCT, SKILL, CONCEPT等
        self.description = description
        self.properties = properties or {}
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.frequency = 1  # 出现频率

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "entity_type": self.entity_type,
            "description": self.description,
            "properties": self.properties,
            "frequency": self.frequency
        }

class Relation:
    """关系类"""

    def __init__(
        self,
        from_entity: str,
        to_entity: str,
        relation_type: str,
        strength: float = 1.0,
        evidence: str = "",
        properties: Dict[str, Any] = None
    ):
        self.from_entity = from_entity
        self.to_entity = to_entity
        self.relation_type = relation_type
        self.strength = strength
        self.evidence = evidence  # 支持该关系的原文本
        self.properties = properties or {}
        self.created_at = datetime.now()
        self.frequency = 1  # 关系出现频率

    def to_dict(self) -> Dict[str, Any]:
        return {
            "from_entity": self.from_entity,
            "to_entity": self.to_entity,
            "relation_type": self.relation_type,
            "strength": self.strength,
            "evidence": self.evidence,
            "properties": self.properties,
            "frequency": self.frequency
        }


class SemanticMemory(BaseMemory):
    """增强语义记忆实现

    特点：
    - 使用HuggingFace中文预训练模型进行文本嵌入
    - 向量检索进行快速相似度匹配
    - 知识图谱存储实体和关系
    - 混合检索策略：向量+图+语义推理
    """

    def __init__(self, config: MemoryConfig, storage_backend=None):
        super().__init__(config, storage_backend)

        # 嵌入模型（统一提供）
        self.embedding_model = None
        self._init_embedding_model()

        # 专业数据库存储
        self.vector_store = None
        self.graph_store = None
        self._init_databases()

        # 实体和关系缓存 (用于快速访问)
        self.entities: Dict[str, Entity] = {}
        self.relations: List[Relation] = []

        # 实体识别器
        self.nlp = None
        self._init_nlp()

        # 记忆存储
        self.semantic_memories: List[MemoryItem] = []
        self.memory_embeddings: Dict[str, np.ndarray] = {}

        logger.warning("增强语义记忆初始化完成（使用Qdrant+Neo4j专业数据库）")

    def _init_embedding_model(self):
        """初始化统一嵌入模型（由 embedding_provider 管理）。"""
        try:
            self.embedding_model = get_text_embedder()
            # 轻量健康检查与日志
            try:
                test_vec = self.embedding_model.encode("health_check")
                dim = getattr(self.embedding_model, "dimension", len(test_vec))
                logger.warning(f"✅ 嵌入模型就绪，维度: {dim}")
            except Exception:
                logger.warning("✅ 嵌入模型就绪")
        except Exception as e:
            logger.error(f"❌ 嵌入模型初始化失败: {e}")
            raise

    def _init_databases(self):
        """初始化专业数据库存储"""
        try:
            from ...core.database_config import get_database_config
            # 获取数据库配置
            db_config = get_database_config()

            # 初始化Qdrant向量数据库（使用连接管理器避免重复连接）
            from ..storage.qdrant_store import QdrantConnectionManager
            qdrant_config = db_config.get_qdrant_config() or {}
            qdrant_config["vector_size"] = get_dimension()
            self.vector_store = QdrantConnectionManager.get_instance(**qdrant_config)
            logger.warning("✅ Qdrant向量数据库初始化完成")

            # 初始化Neo4j图数据库
            from ..storage.neo4j_store import Neo4jGraphStore
            neo4j_config = db_config.get_neo4j_config()
            self.graph_store = Neo4jGraphStore(**neo4j_config)
            logger.warning("✅ Neo4j图数据库初始化完成")

            # 验证连接
            vector_health = self.vector_store.health_check()
            graph_health = self.graph_store.health_check()

            if not vector_health:
                logger.warning("⚠️ Qdrant连接异常，部分功能可能受限")
            if not graph_health:
                logger.warning("⚠️ Neo4j连接异常，图搜索功能可能受限")

            logger.warning(f"🏥 数据库健康状态: Qdrant={'✅' if vector_health else '❌'}, Neo4j={'✅' if graph_health else '❌'}")

        except Exception as e:
            logger.error(f"❌ 数据库初始化失败: {e}")
            logger.warning("💡 请检查数据库配置和网络连接")
            logger.warning("💡 参考 DATABASE_SETUP_GUIDE.md 进行配置")
            raise

    def _init_nlp(self):
        """初始化NLP处理器 - 智能多语言支持"""
        try:
            import spacy
            self.nlp_models = {}

            # 尝试加载多语言模型
            models_to_try = [
                ("zh_core_web_sm", "中文"),
                ("en_core_web_sm", "英文")
            ]

            loaded_models = []
            for model_name, lang_name in models_to_try:
                try:
                    nlp = spacy.load(model_name)
                    self.nlp_models[model_name] = nlp
                    loaded_models.append(lang_name)
                    logger.warning(f"✅ 加载{lang_name}spaCy模型: {model_name}")
                except OSError:
                    logger.warning(f"⚠️ {lang_name}spaCy模型不可用: {model_name}")

            # 设置主要NLP处理器
            if "zh_core_web_sm" in self.nlp_models:
                self.nlp = self.nlp_models["zh_core_web_sm"]
                logger.warning("🎯 主要使用中文spaCy模型")
            elif "en_core_web_sm" in self.nlp_models:
                self.nlp = self.nlp_models["en_core_web_sm"]
                logger.warning("🎯 主要使用英文spaCy模型")
            else:
                self.nlp = None
                logger.warning("⚠️ 无可用spaCy模型，实体提取将受限")

            if loaded_models:
                logger.warning(f"📚 可用语言模型: {', '.join(loaded_models)}")

        except ImportError:
            logger.warning("⚠️ spaCy不可用，实体提取将受限")
            self.nlp = None
            self.nlp_models = {}

    def add(self, memory_item: MemoryItem) -> str:
        """添加语义记忆"""
        try:
            # 1. 生成文本嵌入
            embedding = self.embedding_model.encode(memory_item.content)
            self.memory_embeddings[memory_item.id] = embedding

            # 2. 提取实体和关系
            entities = self._extract_entities(memory_item.content)
            relations = self._extract_relations(memory_item.content, entities)

            # 3. 存储到Neo4j图数据库
            for entity in entities:
                self._add_entity_to_graph(entity, memory_item)

            for relation in relations:
                self._add_relation_to_graph(relation, memory_item)

            # 4. 存储到Qdrant向量数据库
            metadata = {
                "memory_id": memory_item.id,
                "user_id": memory_item.user_id,
                "content": memory_item.content,
                "memory_type": memory_item.memory_type,
                "timestamp": int(memory_item.timestamp.timestamp()),
                "importance": memory_item.importance,
                "entities": [e.entity_id for e in entities],
                "entity_count": len(entities),
                "relation_count": len(relations)
            }

            success = self.vector_store.add_vectors(
                vectors=[embedding.tolist()],
                metadata=[metadata],
                ids=[memory_item.id]
            )

            if not success:
                logger.warning("⚠️ 向量存储失败，但记忆已添加到图数据库")

            # 5. 添加实体信息到元数据
            memory_item.metadata["entities"] = [e.entity_id for e in entities]
            memory_item.metadata["relations"] = [
                f"{r.from_entity}-{r.relation_type}-{r.to_entity}" for r in relations
            ]

            # 6. 存储记忆
            self.semantic_memories.append(memory_item)

            logger.warning(f"✅ 添加语义记忆: {len(entities)}个实体, {len(relations)}个关系")
            return memory_item.id

        except Exception as e:
            logger.error(f"❌ 添加语义记忆失败: {e}")
            raise

    def _detect_language(self, text: str) -> str:
        """简单的语言检测"""
        # 统计中文字符比例（无正则，逐字符判断范围）
        chinese_chars = sum(1 for ch in text if '\u4e00' <= ch <= '\u9fff')
        total_chars = len(text.replace(' ', ''))

        if total_chars == 0:
            return "en"

        chinese_ratio = chinese_chars / total_chars
        return "zh" if chinese_ratio > 0.3 else "en"

    def _extract_entities(self, text: str) -> List[Entity]:
        """智能多语言实体提取"""
        entities = []

        # 检测文本语言
        lang = self._detect_language(text)

        # 选择合适的spaCy模型
        selected_nlp = None
        if lang == "zh" and "zh_core_web_sm" in self.nlp_models:
            selected_nlp = self.nlp_models["zh_core_web_sm"]
        elif lang == "en" and "en_core_web_sm" in self.nlp_models:
            selected_nlp = self.nlp_models["en_core_web_sm"]
        else:
            # 使用默认模型
            selected_nlp = self.nlp

        logger.warning(f"🌐 检测语言: {lang}, 使用模型: {selected_nlp.meta['name'] if selected_nlp else 'None'}")

        # 使用spaCy进行实体识别和词法分析
        if selected_nlp:
            try:
                doc = selected_nlp(text)
                logger.warning(f"📝 spaCy处理文本: '{text}' -> {len(doc.ents)} 个实体")

                # 存储词法分析结果，供Neo4j使用
                self._store_linguistic_analysis(doc, text)

                if not doc.ents:
                    # 如果没有实体，记录详细的词元信息
                    logger.warning("🔍 未找到实体，词元分析:")
                    for token in doc[:5]:  # 只显示前5个词元
                        logger.warning(f"   '{token.text}' -> POS: {token.pos_}, TAG: {token.tag_}, ENT_IOB: {token.ent_iob_}")

                for ent in doc.ents:
                    entity = Entity(
                        entity_id=f"entity_{hash(ent.text)}",
                        name=ent.text,
                        entity_type=ent.label_,
                        description=f"从文本中识别的{ent.label_}实体"
                    )
                    entities.append(entity)
                    # 安全获取置信度信息
                    confidence = "N/A"
                    try:
                        if hasattr(ent._, 'confidence'):
                            confidence = getattr(ent._, 'confidence', 'N/A')
                    except:
                        confidence = "N/A"

                    logger.warning(f"🏷️ spaCy识别实体: '{ent.text}' -> {ent.label_} (置信度: {confidence})")

            except Exception as e:
                logger.warning(f"⚠️ spaCy实体识别失败: {e}")
                import traceback
                logger.warning(f"详细错误: {traceback.format_exc()}")
        else:
            logger.warning("⚠️ 没有可用的spaCy模型进行实体识别")

        return entities

    def _store_linguistic_analysis(self, doc, text: str):
        """存储spaCy词法分析结果到Neo4j"""
        if not self.graph_store:
            return

        try:
            # 为每个词元创建节点
            for token in doc:
                # 跳过标点符号和空格
                if token.is_punct or token.is_space:
                    continue

                token_id = f"token_{hash(token.text + token.pos_)}"

                # 添加词元节点到Neo4j
                self.graph_store.add_entity(
                    entity_id=token_id,
                    name=token.text,
                    entity_type="TOKEN",
                    properties={
                        "pos": token.pos_,        # 词性（NOUN, VERB等）
                        "tag": token.tag_,        # 细粒度标签
                        "lemma": token.lemma_,    # 词元原形
                        "is_alpha": token.is_alpha,
                        "is_stop": token.is_stop,
                        "source_text": text[:50],  # 来源文本片段
                        "language": self._detect_language(text)
                    }
                )

                # 如果是名词，可能是潜在的概念
                if token.pos_ in ["NOUN", "PROPN"]:
                    concept_id = f"concept_{hash(token.text)}"
                    self.graph_store.add_entity(
                        entity_id=concept_id,
                        name=token.text,
                        entity_type="CONCEPT",
                        properties={
                            "category": token.pos_,
                            "frequency": 1,  # 可以后续累计
                            "source_text": text[:50]
                        }
                    )

                    # 建立词元到概念的关系
                    self.graph_store.add_relationship(
                        from_entity_id=token_id,
                        to_entity_id=concept_id,
                        relationship_type="REPRESENTS",
                        properties={"confidence": 1.0}
                    )

            # 建立词元之间的依存关系
            for token in doc:
                if token.is_punct or token.is_space or token.head == token:
                    continue

                from_id = f"token_{hash(token.text + token.pos_)}"
                to_id = f"token_{hash(token.head.text + token.head.pos_)}"

                # Neo4j不允许关系类型包含冒号，需要清理
                relation_type = token.dep_.upper().replace(":", "_")

                self.graph_store.add_relationship(
                    from_entity_id=from_id,
                    to_entity_id=to_id,
                    relationship_type=relation_type,  # 清理后的依存关系类型
                    properties={
                        "dependency": token.dep_,  # 保留原始依存关系
                        "source_text": text[:50]
                    }
                )

            logger.warning(f"🔗 已将词法分析结果存储到Neo4j: {len([t for t in doc if not t.is_punct and not t.is_space])} 个词元")

        except Exception as e:
            logger.warning(f"⚠️ 存储词法分析失败: {e}")

    def _extract_relations(self, text: str, entities: List[Entity]) -> List[Relation]:
        """提取关系"""
        relations = []
        # 仅保留简单共现关系，不做任何正则/关键词匹配
        for i, entity1 in enumerate(entities):
            for entity2 in entities[i+1:]:
                relations.append(Relation(
                    from_entity=entity1.entity_id,
                    to_entity=entity2.entity_id,
                    relation_type="CO_OCCURS",
                    strength=0.5,
                    evidence=text[:100]
                ))
        return relations

    def _add_entity_to_graph(self, entity: Entity, memory_item: MemoryItem):
        """添加实体到Neo4j图数据库"""
        try:
            # 准备实体属性
            properties = {
                "name": entity.name,
                "description": entity.description,
                "frequency": entity.frequency,
                "memory_id": memory_item.id,
                "user_id": memory_item.user_id,
                "importance": memory_item.importance,
                **entity.properties
            }

            # 添加到Neo4j
            success = self.graph_store.add_entity(
                entity_id=entity.entity_id,
                name=entity.name,
                entity_type=entity.entity_type,
                properties=properties
            )

            if success:
                # 同时更新本地缓存
                if entity.entity_id in self.entities:
                    self.entities[entity.entity_id].frequency += 1
                    self.entities[entity.entity_id].updated_at = datetime.now()
                else:
                    self.entities[entity.entity_id] = entity

            return success

        except Exception as e:
            logger.error(f"❌ 添加实体到图数据库失败: {e}")
            return False

    def _add_relation_to_graph(self, relation: Relation, memory_item: MemoryItem):
        """添加关系到Neo4j图数据库"""
        try:
            # 准备关系属性
            properties = {
                "strength": relation.strength,
                "memory_id": memory_item.id,
                "user_id": memory_item.user_id,
                "importance": memory_item.importance,
                "evidence": relation.evidence
            }

            # 添加到Neo4j
            success = self.graph_store.add_relationship(
                from_entity_id=relation.from_entity,
                to_entity_id=relation.to_entity,
                relationship_type=relation.relation_type,
                properties=properties
            )

            if success:
                # 同时更新本地缓存
                self.relations.append(relation)

            return success

        except Exception as e:
            logger.error(f"❌ 添加关系到图数据库失败: {e}")
            return False
