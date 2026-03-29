import unittest
import numpy as np
from perceptron import MultilayerBinaryPerceptron

class TestPerceptron(unittest.TestCase):
    
    def setUp(self):
        # Ця функція запускається перед кожним тестом
        self.mlp = MultilayerBinaryPerceptron(input_size=2, hidden_size=3, output_size=1)

    def test_initialization(self):
        """Тестуємо, чи правильно створюються матриці ваг (відповідно до розмірів)"""
        self.assertEqual(self.mlp.W1.shape, (2, 3), "Невірний розмір матриці W1")
        self.assertEqual(self.mlp.W2.shape, (3, 1), "Невірний розмір матриці W2")

    def test_sigmoid_function(self):
        """Тестуємо функцію активації сигмоїд (sigmoid(0) має дорівнювати 0.5)"""
        result = self.mlp._sigmoid(0)
        self.assertEqual(result, 0.5, "Помилка в обчисленні сигмоїди")

if __name__ == '__main__':
    unittest.main()