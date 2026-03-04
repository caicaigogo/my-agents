import unittest
from dotenv import load_dotenv
import os

from hello_agents.memory.storage import Neo4jGraphStore


class TestNeo4jGraphStore(unittest.TestCase):

    def test_init(self):
        load_dotenv()

        neo4j_uri = os.environ['NEO4J_URI']
        username: str = "neo4j"
        password: str = os.environ['NEO4J_PASSWORD']
        Neo4jGraphStore(uri=neo4j_uri, username=username, password=password)
