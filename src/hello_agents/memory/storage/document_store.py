"""文档存储实现

支持多种文档数据库后端：
- SQLite: 轻量级关系型数据库
- PostgreSQL: 企业级关系型数据库（可扩展）
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import sqlite3
import json
import os
import threading


class DocumentStore(ABC):
    """文档存储基类"""


class SQLiteDocumentStore(DocumentStore):
    """SQLite文档存储实现"""

    _instances = {}  # 存储已创建的实例
    _initialized_dbs = set()  # 存储已初始化的数据库路径

    def __new__(cls, db_path: str = "./memory.db"):
        """单例模式，同一路径只创建一个实例"""
        abs_path = os.path.abspath(db_path)
        if abs_path not in cls._instances:
            instance = super(SQLiteDocumentStore, cls).__new__(cls)
            cls._instances[abs_path] = instance
        return cls._instances[abs_path]

    def __init__(self, db_path: str = "./memory.db"):
        # 避免重复初始化
        if hasattr(self, '_initialized'):
            return

        self.db_path = db_path
        self.local = threading.local()

        # 确保目录存在
        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)

        # 初始化数据库（只初始化一次）
        abs_path = os.path.abspath(db_path)
        if abs_path not in self._initialized_dbs:
            self._init_database()
            self._initialized_dbs.add(abs_path)
            print(f"[OK] SQLite 文档存储初始化完成: {db_path}")

        self._initialized = True

    def _get_connection(self):
        """获取线程本地连接"""
        if not hasattr(self.local, 'connection'):
            self.local.connection = sqlite3.connect(self.db_path)
            self.local.connection.row_factory = sqlite3.Row  # 使结果可以按列名访问
        return self.local.connection

    def _init_database(self):
        """初始化数据库表"""
        conn = self._get_connection()
        cursor = conn.cursor()

        # 创建用户表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                name TEXT,
                properties TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 创建记忆表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                content TEXT NOT NULL,
                memory_type TEXT NOT NULL,
                timestamp INTEGER NOT NULL,
                importance REAL NOT NULL,
                properties TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)

        # 创建概念表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS concepts (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                properties TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 创建记忆-概念关联表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory_concepts (
                memory_id TEXT NOT NULL,
                concept_id TEXT NOT NULL,
                relevance_score REAL DEFAULT 1.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (memory_id, concept_id),
                FOREIGN KEY (memory_id) REFERENCES memories (id) ON DELETE CASCADE,
                FOREIGN KEY (concept_id) REFERENCES concepts (id) ON DELETE CASCADE
            )
        """)

        # 创建概念关系表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS concept_relationships (
                from_concept_id TEXT NOT NULL,
                to_concept_id TEXT NOT NULL,
                relationship_type TEXT NOT NULL,
                strength REAL DEFAULT 1.0,
                properties TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (from_concept_id, to_concept_id, relationship_type),
                FOREIGN KEY (from_concept_id) REFERENCES concepts (id) ON DELETE CASCADE,
                FOREIGN KEY (to_concept_id) REFERENCES concepts (id) ON DELETE CASCADE
            )
        """)

        # 创建索引
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_memories_user_id ON memories (user_id)",
            "CREATE INDEX IF NOT EXISTS idx_memories_type ON memories (memory_type)",
            "CREATE INDEX IF NOT EXISTS idx_memories_timestamp ON memories (timestamp)",
            "CREATE INDEX IF NOT EXISTS idx_memories_importance ON memories (importance)",
            "CREATE INDEX IF NOT EXISTS idx_memory_concepts_memory ON memory_concepts (memory_id)",
            "CREATE INDEX IF NOT EXISTS idx_memory_concepts_concept ON memory_concepts (concept_id)"
        ]

        for index_sql in indexes:
            cursor.execute(index_sql)

        conn.commit()
        print("[OK] SQLite 数据库表和索引创建完成")

    def add_memory(
        self,
        memory_id: str,
        user_id: str,
        content: str,
        memory_type: str,
        timestamp: int,
        importance: float,
        properties: Dict[str, Any] = None
    ) -> str:
        """添加记忆"""
        conn = self._get_connection()
        cursor = conn.cursor()

        # 确保用户存在
        cursor.execute("INSERT OR IGNORE INTO users (id, name) VALUES (?, ?)", (user_id, user_id))

        # 插入记忆
        cursor.execute("""
            INSERT OR REPLACE INTO memories
            (id, user_id, content, memory_type, timestamp, importance, properties, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (
            memory_id,
            user_id,
            content,
            memory_type,
            timestamp,
            importance,
            json.dumps(properties) if properties else None
        ))

        conn.commit()
        return memory_id
