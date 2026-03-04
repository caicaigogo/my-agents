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

    def test_init(self):
        load_dotenv()

        self.config = MemoryConfig()
        self.memory = SemanticMemory(self.config)
