"""
Qdrant向量数据库存储实现
使用专业的Qdrant向量数据库替代ChromaDB
"""

import logging
import threading
from typing import Dict, List, Optional, Any, Union


try:
    from qdrant_client import QdrantClient
    from qdrant_client.http import models
    from qdrant_client.http.models import (
        Distance, VectorParams, PointStruct,
        Filter, FieldCondition, MatchValue, SearchRequest
    )
    QDRANT_AVAILABLE = True
except ImportError:
    QDRANT_AVAILABLE = False
    QdrantClient = None
    models = None

logger = logging.getLogger(__name__)


class QdrantConnectionManager:
    """Qdrant连接管理器 - 防止重复连接和初始化"""
    _instances = {}  # key: (url, collection_name) -> QdrantVectorStore instance
    _lock = threading.Lock()

    @classmethod
    def get_instance(
        cls,
        url: Optional[str] = None,
        api_key: Optional[str] = None,
        collection_name: str = "hello_agents_vectors",
        vector_size: int = 384,
        distance: str = "cosine",
        timeout: int = 30,
        **kwargs
    ) -> 'QdrantVectorStore':
        """获取或创建Qdrant实例（单例模式）"""
        # 创建唯一键
        key = (url or "local", collection_name)

        if key not in cls._instances:
            with cls._lock:
                # 双重检查锁定
                if key not in cls._instances:
                    logger.debug(f"🔄 创建新的Qdrant连接: {collection_name}")
                    cls._instances[key] = QdrantVectorStore(
                        url=url,
                        api_key=api_key,
                        collection_name=collection_name,
                        vector_size=vector_size,
                        distance=distance,
                        timeout=timeout,
                        **kwargs
                    )
                else:
                    logger.debug(f"♻️ 复用现有Qdrant连接: {collection_name}")
        else:
            logger.debug(f"♻️ 复用现有Qdrant连接: {collection_name}")

        return cls._instances[key]

class QdrantVectorStore:
    """Qdrant向量数据库存储实现"""

    def __init__(
        self,
        url: Optional[str] = None,
        api_key: Optional[str] = None,
        collection_name: str = "hello_agents_vectors",
        vector_size: int = 384,
        distance: str = "cosine",
        timeout: int = 30,
        **kwargs
    ):
        """
        初始化Qdrant向量存储 (支持云API)

        Args:
            url: Qdrant云服务URL (如果为None则使用本地)
            api_key: Qdrant云服务API密钥
            collection_name: 集合名称
            vector_size: 向量维度
            distance: 距离度量方式 (cosine, dot, euclidean)
            timeout: 连接超时时间
        """
        if not QDRANT_AVAILABLE:
            raise ImportError(
                "qdrant-client未安装。请运行: pip install qdrant-client>=1.6.0"
            )

        self.url = url
        self.api_key = api_key
        self.collection_name = collection_name
        self.vector_size = vector_size
        self.timeout = timeout
