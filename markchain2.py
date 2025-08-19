import os
from markovchains import MarkovChain
from tokenizer import Tokenizer
import numpy as np
import time


data_path = os.path.dirname(__file__) + "/data/onegin_clear.txt"
tokens_path = os.path.dirname(__file__) + "/data/onegin_tokenized.txt"
tokenizer = Tokenizer(data_path, 4, 2)
tokenizer.tokenize_file(data_path, tokens_path)

# print(tokenizer.token_num)
model = MarkovChain(list(range(tokenizer.token_num)))
model_file = "MarkChain+Tokenizer.npz"
# model.train_tokenized(tokens_path, save_model_file=model_file)
model.from_file(model_file)
seq = model.generate_sequence(np.random.choice(range(tokenizer.token_num)), 200)
print(tokenizer.detokenize(seq))

