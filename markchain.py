import os
import re
import sys
import random
import numpy as np

class MarkovChain:
    def __init__(self, states, transition_matrix):
        """
        Инициализация Марковской цепи.
        
        :param states: список состояний
        :param transition_matrix: матрица переходов (двумерный список)
        """
        self.states = states
        self.transition_matrix = np.ones((len(states), len(states))) / len(states)
        self.state_index = {state: idx for idx, state in enumerate(states)}
        self.validate_transition_matrix()

    def validate_transition_matrix(self):
        """Проверка корректности матрицы переходов."""
        n = len(self.states)
        if len(self.transition_matrix) != n:
            raise ValueError("Число строк матрицы должно соответствовать количеству состояний")
        
        for i, row in enumerate(self.transition_matrix):
            if len(row) != n:
                raise ValueError(f"Строка {i} имеет неверную длину")
            
            total = sum(row)
            if not (0.99 < total < 1.01):  # Допустимая погрешность
                raise ValueError(f"Сумма вероятностей в строке {i} ({total}) не равна 1")

    
    def train(self, data_path):
        with open(data_path, 'r', encoding='utf-8') as f_in:
        
            data = [line for line in open(data_path, 'r', encoding='utf-8')]
            states = model.states 
            st2tok = {states[i]: i for i in range(len(states))}

            M = np.zeros((len(states), len(states)), dtype=np.float64)
            for batch_idx, batch in enumerate(data):
                for i in range(len(batch) - 1):
                    M[st2tok[batch[i]], st2tok[batch[i+1]]] += 1
                if batch_idx < len(data) - 1:
                    M[st2tok[batch[-1]], st2tok[data[batch_idx+1][0]]] += 1
                
            M = normalize(M)
            f_in.close()
        self.transition_matrix = M

    def next_state(self, current_state):
        """
        Возвращает следующее состояние на основе текущего состояния.
        
        :param current_state: текущее состояние
        :return: следующее состояние
        """
        if current_state not in self.state_index:
            raise ValueError(f"Неизвестное состояние: {current_state}")
        
        current_idx = self.state_index[current_state]
        probabilities = self.transition_matrix[current_idx]
        
        # Выбор следующего состояния с учетом вероятностей
        if sum(probabilities) == 0:
            raise ValueError(f"Что-то не так с обучением: {current_state, current_idx}")

        next_idx = random.choices(
            population=range(len(self.states)),
            weights=probabilities,
            k=1
        )[0]
        
        return self.states[next_idx]

    def generate_sequence(self, start_state, length):
        """
        Генерирует последовательность состояний заданной длины.
        
        :param start_state: начальное состояние
        :param length: длина последовательности
        :return: список состояний
        """
        if start_state not in self.state_index:
            raise ValueError(f"Неизвестное начальное состояние: {start_state}")
        
        sequence = [start_state]
        current_state = start_state
        
        for _ in range(length - 1):
            current_state = self.next_state(current_state)
            sequence.append(current_state)
            
        return sequence

def clear_data(input_file, output_file):
    # Все русские буквы (кириллица) в обоих регистрах
    russian_letters = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    
    # Основные знаки пунктуации (включая специфические для русского языка)
    punctuation = "!\"',-.:?"
    
    # Символы новой строки и возврата каретки (для обработки разных форматов)
    newlines = "\n "
    
    # Объединяем все разрешенные символы
    allowed_chars = russian_letters + punctuation + newlines
    
    # Преобразуем в множество для быстрого поиска
    allowed_set = set(allowed_chars)
    
    # Обрабатываем файл построчно
    with open(input_file, 'r', encoding='utf-8') as f_in, \
         open(output_file, 'w', encoding='utf-8') as f_out:
        
        for line in f_in:
            # Фильтруем символы в строке
            filtered_line = ''.join(char for char in line if char in allowed_set)
            f_out.write(filtered_line)



def normalize(mat):
    X = mat.copy()
    X_next = X.copy()
    eps = 1
    # while eps > 0.001:
    #     X_next = X.copy()
        # for i in range(X.shape[0]):
        #     if sum(X[i, :]) != 0:
        #         X_next[i, :] = X[i, :] / sum(X[i, :])
    for j in range(X_next.shape[1]):
        if sum(X_next[:, j]) != 0:
            X_next[:, j] = X_next[:, j] / sum(X_next[:, j])

        # eps = abs(max((X_next - X).flatten()))
    X = X_next
    return X
        

# regex = re.compile(r'[\t\r]')
# file = [regex.sub("", line) for line in open()]
data_dirty = os.path.dirname(__file__) + "/data/onegin.txt"
data_path = os.path.dirname(__file__) + "/data/onegin_clear.txt"
clear_data(data_dirty, data_path)
letters = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ" + "!\"',-.:?" + "\n "

model = MarkovChain(letters, np.zeros((len(letters), len(letters)), dtype=np.float64))
model.train(data_path)
print("".join(model.generate_sequence("Х", 100)))