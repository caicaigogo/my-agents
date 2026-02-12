import unittest

from hello_agents.tools.builtin.calculator import calculate


class TestCalculatorTool(unittest.TestCase):

    def test_calculate_function(self):

        self.assertEqual('5', calculate('5'))
        self.assertEqual('8', calculate('5+3'))
        self.assertEqual('15', calculate('5 * 3'))
        self.assertEqual('1.2', calculate('6/5'))
        self.assertEqual('8', calculate('2**3'))
        self.assertEqual('0', calculate('1^1'))

        self.assertEqual('-1', calculate('-1'))

        self.assertEqual('5', calculate('abs(-5)'))
        self.assertEqual('3', calculate('round(3.4)'))
        self.assertEqual('4', calculate('round(3.5)'))

        self.assertEqual('8', calculate('max(3, -1, 8)'))
        self.assertEqual('-1', calculate('min(3, -1, 8)'))
        self.assertEqual('0.4', calculate('sqrt(0.16)'))
        self.assertEqual('0.0', calculate('sin(0)'))
        self.assertEqual('1.0', calculate('cos(0)'))
        self.assertEqual('0.0', calculate('tan(0)'))
        self.assertEqual('0.0', calculate('log(1)'))
        self.assertEqual('1.0', calculate('exp(0)'))
        self.assertEqual('3.141592653589793', calculate('pi'))
        self.assertEqual('2.718281828459045', calculate('e'))
