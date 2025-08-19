import numpy as np
import os

class Tokenizer:

    def __init__(self, data_path, n_gramm=4, sliding=0):
    
        self.seq2tok = dict()
        self.tok2seq = dict()
        self.n_gramm = n_gramm
        self.sliding = sliding
        self.token_num = 0


        with open(data_path, 'r', encoding='utf-8') as file:
            self.token_num = 0
            buffer = ""
            for line in file.readlines():
                i = 0
                while i < len(line) - n_gramm + 1:
                    buffer += line[i: i + n_gramm]
                    i += n_gramm - sliding
                    if not(buffer in self.seq2tok.keys()):
                        self.seq2tok[buffer] = self.token_num
                        self.tok2seq[self.token_num] = buffer
                        self.token_num += 1
                # print(buffer)
                    buffer = ""
        self.token_num += 1 # for unknown tokens

    def tokenize_text(self, text, f_out=None):
        if f_out:
            tokens = open(f_out, 'w')
        else:
            tokens = []
        for i in range(0, len(text) - self.n_gramm + 1, self.n_gramm - self.sliding):
            seq = text[i:i + self.n_gramm]
            if seq in self.seq2tok.keys():
                if f_out:
                    tokens.write(self.seq2tok[seq])
                tokens.append(self.seq2tok[seq])
            else:
                tokens.append(-1)
        return tokens


    def tokenize_file(self, data_in, data_out):
        with open(data_in, 'r') as f_in, open(data_out, 'w') as f_out:
            for line in f_in.readlines():
                for i in range(0, len(line) - self.n_gramm + 1, self.n_gramm - self.sliding):
                    seq = line[i:i + self.n_gramm]
                    if seq in self.seq2tok.keys():
                        # print(self.seq2tok[seq])
                        f_out.write(str(self.seq2tok[seq]) + "\n")
                    else:
                        # print(-1)
                        f_out.write(str(-1) + "\n")
    
    def tokenize_modified(self, data_in, data_out=""):
        with open(data_in, 'r') as f_in, open(data_out, 'w') as f_out:
             
            for line in text:
                words = line.split()
                tokens = []
                for word in words:
                    if len(word) < 3:
                        tokens.append(word)
                        continue
                    if word[:2] in ["за", "вы", "не", "из", "по", "на", "от", "вз", "вс", "до", "ре", "де"]:
                        tokens.append(word[:2])
                    elif word[:3] in ["без", "бес", "воз", "вос", "изо", "нис", "низ", "обо", "пре", "при", "про", "раз", "рас", "вне", "меж", "пра"]:
                        tokens.append(word[:3])
                    tokens.append(word[2:-2])
                    tokens.append(word[-3:])

    

    def detokenize(self, tokens):
        seq = self.tok2seq[tokens[0]]
        for i in range(1, len(tokens)):
            if not (tokens[i] in self.tok2seq.keys()):
                if tokens[i] == -1:
                    seq += "*" * self.n_gramm
                    continue
                else:
                    raise ValueError(f"Token {tokens[i]} is not recognized")
            text = self.tok2seq[tokens[i]]
            # print(text)
            if seq[-self.sliding:] == text[:self.sliding]:
                seq += text[self.sliding:]
            else:
                seq += '\n' + text
        return seq
        



# data_path = os.path.dirname(__file__) + "/data/onegin_clear.txt"
# data_out = os.path.dirname(__file__) + "/output/test.txt"
# tok = Tokenizer(data_path, 4, 1)
# tok.tokenize(data_path, data_out)
# print(tok.seq2tok)

text = ["Как на досадную разлуку,\n", 
        "Татьяна ропщет на ручей\n",
        "Не видит никого, кто руку\n", 
        "С той стороны подал бы ей\n", 
        "Но вдруг сугроб зашевелился,\n", 
        "И кто ж из-под него явился?\0"]

for line in text:
    words = line.split()
    tokens = []
    for word in words:
        if len(word) < 3:
            tokens.append(word)
            continue
        if word[:2] in ["за", "вы", "не", "из", "по", "на", "от", "вз", "вс", "до", "ре", "де"]:
            tokens.append(word[:2])
        elif word[:3] in ["без", "бес", "воз", "вос", "изо", "нис", "низ", "обо", "пре", "при", "про", "раз", "рас", "вне", "меж", "пра"]:
            tokens.append(word[:3])
        tokens.append(word[2:-2])
        tokens.append(word[-3:])
    