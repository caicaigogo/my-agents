import unittest
from hello_agents.memory.embedding import TFIDFEmbedding


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
