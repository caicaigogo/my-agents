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


    def _initialize_driver(self, **config):
        """初始化Neo4j驱动"""
        try:
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=(self.username, self.password),
                **config
            )

        except Exception as e:
            logger.error(f"❌ Neo4j连接失败: {e}")
            raise

