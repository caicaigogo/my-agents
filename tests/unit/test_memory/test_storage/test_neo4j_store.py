import unittest
from dotenv import load_dotenv
import os

from neo4j import GraphDatabase


class TestNeo4jGraphStore(unittest.TestCase):

    def test_init(self):
        load_dotenv()

        neo4j_uri = os.environ['neo4j_uri']
        username: str = "neo4j"
        password: str = os.environ['neo4j_password']

        self.driver = GraphDatabase.driver(
            neo4j_uri,
            auth=(username, password),
        )

        print(self.driver)
