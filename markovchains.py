import os
import re
import sys
import random
import numpy as np
from tqdm import tqdm
from scipy.sparse import csr_matrix, lil_array, save_npz, load_npz, dok_array
from scipy.sparse.linalg import eigs

class MarkovChain:
    def __init__(self, states, transition_matrix=0):
        """
        Инициализация Марковской цепи.
        
        :param states: список состояний
        :param transition_matrix: матрица переходов (двумерный список)
        """
        self.states = states
        # if transition_matrix == 0:
        #     self.transition_matrix = np.ones((len(states), len(states)), dtype=np.float64) / len(states)
        # else:
        #     self.transition_matrix = transition_matrix
        self.state_index = {state: idx for idx, state in enumerate(states)}
        self.init_prob = np.ones((1, len(states)), dtype=np.float64) / len(states)
        # self.validate_transition_matrix()

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
            data = [line for line in f_in]
            states = self.states 
            M = csr_matrix((len(states), len(states)), dtype=np.float64)
            for batch_idx, batch in tqdm(enumerate(data)):
                for i in range(len(batch) - 1):
                    M[self.state_index[int(batch[i])], self.state_index[int(batch[i+1])]] += 1
                if batch_idx < len(data) - 1:
                    M[self.state_index[int(batch[-1])], self.state_index[int(data[batch_idx+1][0])]] += 1
                
            M = self.normalize(M)
        self.transition_matrix = M


    def train_tokenized(self, data_path, save_model_file=None):
        with open(data_path, 'r', encoding='utf-8') as f_in:
            data = [token.replace("\n", '') for token in f_in]
            states = self.states 
            M = csr_matrix((len(states), len(states)), dtype=np.float64)
            print("Training...")
            for token_idx, token in tqdm(enumerate(data)):
                if token_idx == len(data) - 1:
                    break    
                M[int(token), int(data[token_idx + 1])] += 1
            M = self.normalize(M)
        self.transition_matrix = M
        # self.init_prob = np.round(-1 * eigs(self.transition_matrix.T, k=1)[-1].real.flatten(), decimals=6)
        # self.init_prob = self.init_prob / sum(self.init_prob)
        if save_model_file:
            save_npz(os.path.dirname(__file__) + "/models/" + save_model_file, M)
        

    def next_state(self, current_state):
        """
        Возвращает следующее состояние на основе текущего состояния.
        
        :param current_state: текущее состояние
        :return: следующее состояние
        """
        if current_state not in self.state_index:
            if current_state == -1:
                return -1
            raise ValueError(f"Неизвестное состояние: {current_state}")
        
        current_idx = self.state_index[current_state]
        probabilities = self.transition_matrix[current_idx].toarray()
        
        # Выбор следующего состояния с учетом вероятностей
        if sum(probabilities[0]) == 0:
            # raise ValueError(f"Что-то не так с обучением: {current_state, current_idx}")
            return -1

        # print(len(self.states), len(probabilities[0]))
        next_idx = random.choices(
            population=range(len(self.states)),
            weights=probabilities[0],
            k=1
        )[0]
        
        return self.states[next_idx]

    def generate_sequence(self, start_state, length, cool=False):
        """
        Генерирует последовательность состояний заданной длины.
        
        :param start_state: начальное состояние
        :param length: длина последовательности
        :return: список состояний
        """
        if not (start_state in self.state_index.keys()):
            raise ValueError(f"Неизвестное начальное состояние: {start_state}")
        
        sequence = [start_state]
        current_state = start_state
        
        print("Generating...")
        for _ in tqdm(range(length - 1)):
            current_state = self.next_state(current_state)
            sequence.append(current_state)
        return sequence

    def normalize(self, mat):
        X_next = mat.copy()
        for i in range(X_next.shape[0]):
            if sum(X_next[i].toarray().flatten()) != 0:
                X_next[i] = X_next[i].multiply(1 / sum(X_next[i].toarray().flatten()))
        return X_next


    def from_file(self, model_file):
        self.transition_matrix = load_npz(os.path.dirname(__file__) + "/models/" + model_file)


# sparse_prob = lil_array((3, 3), dtype=np.float64)
# sparse_prob[0, 1] += 2
# sparse_prob[0, 0] += 1
# sparse_prob[1, 2] += 2
# sparse_prob[2, 0] += 2
# sparse_prob[2, 2] += 3
# print(sparse_prob.toarray())
# print(eigs(sparse_prob.T, k=1))