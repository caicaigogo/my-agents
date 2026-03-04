"""
Neo4j图数据库存储实现
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime

try:
    from neo4j import GraphDatabase
    from neo4j.exceptions import ServiceUnavailable, AuthError
    NEO4J_AVAILABLE = True
except ImportError:
    NEO4J_AVAILABLE = False
    GraphDatabase = None

logger = logging.getLogger(__name__)

class Neo4jGraphStore:
    """Neo4j图数据库存储实现"""

    def __init__(
        self,
        uri: str = "bolt://localhost:7687",
        username: str = "neo4j",
        password: str = "hello-agents-password",
        database: str = "neo4j",
        max_connection_lifetime: int = 3600,
        max_connection_pool_size: int = 50,
        connection_acquisition_timeout: int = 60,
        **kwargs
    ):
        """
        初始化Neo4j图存储 (支持云API)

        Args:
            uri: Neo4j连接URI (本地: bolt://localhost:7687, 云: neo4j+s://xxx.databases.neo4j.io)
            username: 用户名
            password: 密码
            database: 数据库名称
            max_connection_lifetime: 最大连接生命周期(秒)
            max_connection_pool_size: 最大连接池大小
            connection_acquisition_timeout: 连接获取超时(秒)
        """
        if not NEO4J_AVAILABLE:
            raise ImportError(
                "neo4j未安装。请运行: pip install neo4j>=5.0.0"
            )

        self.uri = uri
        self.username = username
        self.password = password
        self.database = database

        # 初始化驱动
        self.driver = None
        self._initialize_driver(
            max_connection_lifetime=max_connection_lifetime,
            max_connection_pool_size=max_connection_pool_size,
            connection_acquisition_timeout=connection_acquisition_timeout
        )

        # 创建索引
        self._create_indexes()

    def _initialize_driver(self, **config):
        """初始化Neo4j驱动"""
        try:
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=(self.username, self.password),
                **config
            )

            # 验证连接
            self.driver.verify_connectivity()

            # 检查是否是云服务
            if "neo4j.io" in self.uri or "aura" in self.uri.lower():
                logger.warning(f"✅ 成功连接到Neo4j云服务: {self.uri}")
            else:
                logger.warning(f"✅ 成功连接到Neo4j服务: {self.uri}")

        except AuthError as e:
            logger.error(f"❌ Neo4j认证失败: {e}")
            logger.warning("💡 请检查用户名和密码是否正确")
            raise
        except ServiceUnavailable as e:
            logger.error(f"❌ Neo4j服务不可用: {e}")
            if "localhost" in self.uri:
                logger.warning("💡 本地连接失败，可以考虑使用Neo4j Aura云服务")
                logger.warning("💡 或启动本地服务: docker run -p 7474:7474 -p 7687:7687 neo4j:5.14")
            else:
                logger.warning("💡 请检查URL和网络连接")
            raise
        except Exception as e:
            logger.error(f"❌ Neo4j连接失败: {e}")
            raise

    def _create_indexes(self):
        """创建必要的索引以提高查询性能"""
        indexes = [
            # 实体索引
            "CREATE INDEX entity_id_index IF NOT EXISTS FOR (e:Entity) ON (e.id)",
            "CREATE INDEX entity_name_index IF NOT EXISTS FOR (e:Entity) ON (e.name)",
            "CREATE INDEX entity_type_index IF NOT EXISTS FOR (e:Entity) ON (e.type)",

            # 记忆索引
            "CREATE INDEX memory_id_index IF NOT EXISTS FOR (m:Memory) ON (m.id)",
            "CREATE INDEX memory_type_index IF NOT EXISTS FOR (m:Memory) ON (m.memory_type)",
            "CREATE INDEX memory_timestamp_index IF NOT EXISTS FOR (m:Memory) ON (m.timestamp)",
        ]

        with self.driver.session(database=self.database) as session:
            for index_query in indexes:
                try:
                    session.run(index_query)
                except Exception as e:
                    logger.warning(f"索引创建跳过 (可能已存在): {e}")

        logger.warning("✅ Neo4j索引创建完成")

    def add_entity(self, entity_id: str, name: str, entity_type: str, properties: Dict[str, Any] = None) -> bool:
        """
        添加实体节点

        Args:
            entity_id: 实体ID
            name: 实体名称
            entity_type: 实体类型
            properties: 附加属性

        Returns:
            bool: 是否成功
        """
        try:
            props = properties or {}
            props.update({
                "id": entity_id,
                "name": name,
                "type": entity_type,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            })

            query = """
            MERGE (e:Entity {id: $entity_id})
            SET e += $properties
            RETURN e
            """

            with self.driver.session(database=self.database) as session:
                result = session.run(query, entity_id=entity_id, properties=props)
                record = result.single()

                if record:
                    logger.warning(f"✅ 添加实体: {name} ({entity_type})")
                    return True
                return False

        except Exception as e:
            logger.error(f"❌ 添加实体失败: {e}")
            return False

    def add_relationship(
        self,
        from_entity_id: str,
        to_entity_id: str,
        relationship_type: str,
        properties: Dict[str, Any] = None
    ) -> bool:
        """
        添加实体间关系

        Args:
            from_entity_id: 源实体ID
            to_entity_id: 目标实体ID
            relationship_type: 关系类型
            properties: 关系属性

        Returns:
            bool: 是否成功
        """
        try:
            props = properties or {}
            props.update({
                "type": relationship_type,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            })

            query = f"""
            MATCH (from:Entity {{id: $from_id}})
            MATCH (to:Entity {{id: $to_id}})
            MERGE (from)-[r:{relationship_type}]->(to)
            SET r += $properties
            RETURN r
            """

            with self.driver.session(database=self.database) as session:
                result = session.run(
                    query,
                    from_id=from_entity_id,
                    to_id=to_entity_id,
                    properties=props
                )
                record = result.single()

                if record:
                    logger.warning(f"✅ 添加关系: {from_entity_id} -{relationship_type}-> {to_entity_id}")
                    return True
                return False

        except Exception as e:
            logger.error(f"❌ 添加关系失败: {e}")
            return False

    def health_check(self) -> bool:
        """
        健康检查

        Returns:
            bool: 服务是否健康
        """
        try:
            with self.driver.session(database=self.database) as session:
                result = session.run("RETURN 1 as health")
                record = result.single()
                return record["health"] == 1
        except Exception as e:
            logger.error(f"❌ Neo4j健康检查失败: {e}")
            return False

    def __del__(self):
        """析构函数，清理资源"""
        if hasattr(self, 'driver') and self.driver:
            try:
                self.driver.close()
            except:
                pass
