import numpy as np
import logging

class MultilayerBinaryPerceptron:
    def __init__(self, input_size=2, hidden_size=2, output_size=1, learning_rate=0.1):
        """
        Ініціалізація нейромережі.
        За замовчуванням: 2 входи (для логічних операцій), 2 нейрони в прихованому шарі, 1 вихід.
        """
        self.learning_rate = learning_rate
        
        # Ініціалізація ваг та зсувів (біасів) випадковими значеннями від -1 до 1
        self.W1 = np.random.uniform(-1, 1, (input_size, hidden_size))
        self.b1 = np.random.uniform(-1, 1, (1, hidden_size))
        
        self.W2 = np.random.uniform(-1, 1, (hidden_size, output_size))
        self.b2 = np.random.uniform(-1, 1, (1, output_size))
        
        logging.info(f"Створено ББП: Входи={input_size}, Приховані={hidden_size}, Виходи={output_size}")

    def _sigmoid(self, x):
        # Функція активації
        return 1 / (1 + np.exp(-x))

    def _sigmoid_derivative(self, x):
        # Похідна для зворотного поширення помилки
        return x * (1 - x)

    def forward(self, X):
        """Пряме поширення: пропускаємо дані через мережу"""
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = self._sigmoid(self.z1)
        
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = self._sigmoid(self.z2)
        return self.a2

    def backward(self, X, y, output):
        """Зворотне поширення: обчислюємо помилку та оновлюємо ваги"""
        error = y - output
        d_output = error * self._sigmoid_derivative(output)
        
        error_hidden = d_output.dot(self.W2.T)
        d_hidden = error_hidden * self._sigmoid_derivative(self.a1)
        
        # Оновлення ваг
        self.W2 += self.a1.T.dot(d_output) * self.learning_rate
        self.b2 += np.sum(d_output, axis=0, keepdims=True) * self.learning_rate
        self.W1 += X.T.dot(d_hidden) * self.learning_rate
        self.b1 += np.sum(d_hidden, axis=0, keepdims=True) * self.learning_rate

    def train(self, X, y, epochs):
        """Навчання мережі задану кількість епох"""
        logging.info(f"Початок навчання. Епох: {epochs}, Швидкість навчання: {self.learning_rate}")
        for epoch in range(epochs):
            output = self.forward(X)
            self.backward(X, y, output)
        logging.info("Навчання успішно завершено.")

    def predict(self, X):
        """Прогнозування результату (повертає 0 або 1)"""
        output = self.forward(X)
        return (output > 0.5).astype(int) # Бінарний поріг