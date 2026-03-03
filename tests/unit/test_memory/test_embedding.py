import unittest
from dotenv import load_dotenv
import os
from hello_agents.memory.embedding import TFIDFEmbedding, DashScopeEmbedding


class TestTFIDFEmbedding(unittest.TestCase):

    def setUp(self):

        self.embedder = TFIDFEmbedding()

    def test_encode(self):

        fit_list = ['hello, nice to meet you', 'how are you', 'i am so happy to meet you']
        self.embedder.fit(fit_list)

        encode_result = self.embedder.encode(fit_list)

        # [array([0., 0.62276601, 0.4736296, 0.62276601]), array([0., 0., 0., 0.]),
        #  array([0.79596054, 0., 0.60534851, 0.])]
        print(encode_result)

        # 4
        print(self.embedder.dimension)

        encode_result = self.embedder.encode(fit_list[0])

        #  [0.         0.62276601 0.4736296  0.62276601]
        print(encode_result)
        # <class 'numpy.ndarray'>
        print(type(encode_result))

        # <class 'list'>
        print(type(encode_result.tolist()))


class TestDashScopeEmbedding(unittest.TestCase):

    def setUp(self):
        load_dotenv()
        api_key = os.environ['jina_API_KEY']
        base_url = 'https://api.jina.ai/v1'
        self.embedder = DashScopeEmbedding(
            model_name='jina-embeddings-v5-text-small', base_url=base_url, api_key=api_key
        )

    def test_encode(self):

        texts = ["Organic skincare for sensitive skin with aloe vera and chamomile: Imagine the soothing embrace of nature with our organic skincare range, crafted specifically for sensitive skin. Infused with the calming properties of aloe vera and chamomile, each product provides gentle nourishment and protection. Say goodbye to irritation and hello to a glowing, healthy complexion."]
        encode_result = self.embedder.encode(texts)

        # [array([0.02411918, 0.01061533, -0.04448329, ..., -0.04101706,
        #         0.05199345, 0.03004066], shape=(1024,))]
        print(encode_result)

        # 1024
        print(self.embedder.dimension)
