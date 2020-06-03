import os
import copy
import glob
import pathlib
import collections

import numpy as np


class Dictionary:

    class Dataset:
        dict_dir = "../dict"
        dict_list = list(map(lambda x: pathlib.PurePath(x).stem, glob.glob(f"{dict_dir}/*.txt")))           

        def __getattr__(self, name):
            if name not in (self.dict_list):
                raise AttributeError(f"{name} must be an element of the 'dict_list'")
            return Dictionary(f"{self.dict_dir}/{name}.txt")

    dataset = Dataset()

    def __init__(self, dict_specifier=None, word=None, weight=None, name=None):
        self.dict_specifier = dict_specifier
        self.size = 0
        self.name = ''
        self.word = []
        self.weight = []
        self.w_len = []
        self.removed_words = []
        if isinstance(dict_specifier, (list, np.ndarray)):
            self.add(dict_specifier)
        if isinstance(dict_specifier, str):
            self.name = os.path.basename(dict_specifier)[:-4]
            self.read(dict_specifier)
        if word is not None:
            self.add(word, weight)
        if name is not None:
            self.name = name
        self._i = 0

    def __getitem__(self, key):
        return {'word': self.word[key], 'weight': self.weight[key], 'len': self.w_len[key]}

    def __str__(self):
        return str({"name": self.name, "words": self.word, "weight": self.weight})

    def __len__(self):
        return self.size

    def __add__(self, other):
        new_dict = copy.deepcopy(self)
        if isinstance(other, Dictionary):
            for wo, we in zip(other.word, other.weight):
                new_dict.add(word = wo, weight = we)
        if isinstance(other, str):
            new_dict.add(word = other, weight = 0)
        if isinstance(other, (tuple, list)):
            new_dict.add(word = other[0], weight = other[1])
        if isinstance(other, dict):
            new_dict.add(word = other["word"], weight = other["weight"])
        return new_dict

    def __iter__(self):
        return self

    def __next__(self):
        if self._i == self.size:
            self._i = 0
            raise StopIteration()
        word, weight = self.word[self._i], self.weight[self._i]
        self._i += 1
        return word, weight
    
    def getK(self, word):
        return np.where(self.word == word)[0][0]

    def include(self, word):
        return word in self.word

    def add(self, word=None, weight=None, dict_specifier=None):
        if (word,dict_specifier) == (None,None):
            raise ValueError("'word' or 'dict_specifier' must be specified")
        if word is dict_specifier is not None:
            raise ValueError("'word' or 'dict_specifier' must be specified")
        if dict_specifier is not None:
            self.read(dict_specifier)
        if word is not None:
            if isinstance(word, str):
                word = [word]
            if weight is None:
                weight = [0]*len(word)
            else:
                if isinstance(weight, int):
                    weight = [weight]
                if len(word) != len(weight):
                    raise ValueError(f"'word' and 'weight' must be same size")
            for wo, we in zip(word, weight):
                if self.include(wo) is True: # replace the weight
                    self.weight[self.word.index(wo)] = we
                else:
                    self.word.append(wo)
                    self.weight.append(we)
                    self.w_len.append(len(wo))
                    self.size += 1

    def read(self, dict_specifier):
        with open(dict_specifier, 'r', encoding='utf-8') as f:
            data = f.readlines()

        # Remove "\n"
        def removed_new_line_code(word):
            line = word.rstrip("\n").split(" ")
            if len(line) == 1:
                line.append(0)
            line[1] = int(line[1])
            return line

        dic_list = list(map(removed_new_line_code, data))
        word = [d[0] for d in dic_list]
        weight = [d[1] for d in dic_list]
        self.add(word, weight)

    def delete_unusable_words(self):
        """
        This method checks words in the dictionary and erases words that can not cross any other words.
        """
        merged_words = "".join(self.word)
        counts = collections.Counter(merged_words)
        for i, w in enumerate(self.word[:]):
            char_value = 0
            for char in set(w):
                char_value += counts[char]
            if char_value == len(w):
                self.removed_words.append(w)
                del self.word[i]
                del self.weight[i]
                del self.w_len[i]
                self.size -= 1

    def calc_weight(self):
        """
        Calculate word weights in the dictionary.
        """
        merged_words = "".join(self.word)
        counts = collections.Counter(merged_words)

        for i, w in enumerate(self.word):
            for char in w:
                self.weight[i] += counts[char]
