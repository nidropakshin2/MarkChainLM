import os
from markovchains import MarkovChain
from tokenizer import Tokenizer
import numpy as np
import time

n_gramm = 4
sliding = 2

data_path = os.path.dirname(__file__) + "/data/onegin_clear.txt"
tokens_path = os.path.dirname(__file__) + f"/data/onegin_tokenized_{n_gramm}_{sliding}.txt"
tokenizer = Tokenizer(data_path, n_gramm, sliding)
tokenizer.tokenize_file(data_path, tokens_path)

# print(tokenizer.token_num)
model = MarkovChain(list(range(tokenizer.token_num)))
model_file = f"MarkChain+Tokenizer_{n_gramm}_{sliding}.npz"
train = False
if train:
    model.train_tokenized(tokens_path, save_model_file=model_file)
else:
    model.from_file(model_file)
    seq_len = 100
    seq = model.generate_sequence(np.random.choice(range(tokenizer.token_num)), 40)
    print(tokenizer.detokenize(seq))

