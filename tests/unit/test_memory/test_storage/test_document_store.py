import unittest

import os
from hello_agents.memory.storage import SQLiteDocumentStore


class TestSQLiteDocumentStore(unittest.TestCase):

    def test_init(self):
        # 权威文档存储（SQLite）
        db_dir = "./memory_data"
        os.makedirs(db_dir, exist_ok=True)
        db_path = os.path.join(db_dir, "memory.db")
        self.doc_store = SQLiteDocumentStore(db_path=db_path)
