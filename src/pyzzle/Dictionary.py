import os
import sys
import copy
from glob import glob
from pathlib import PurePath
import collections

import numpy as np

from pyzzle.Word import Word


class Dictionary:
    class Dataset:
        dict_dir = str(PurePath(__file__).parent/PurePath("dict"))
        dict_list = list(map(lambda x: PurePath(x).stem, glob(f"{dict_dir}/*.txt")))

        def __getattr__(self, key):
            if key not in self.dict_list:
                raise AttributeError(f"{key} must be an element of the 'dict_list'")
            return Dictionary(f"{self.dict_dir}/{key}.txt")

        def __getitem__(self, key):
            return Dictionary(f"{self.dict_dir}/{key}.txt")

    dataset = Dataset()

    def __init__(self, dict_specifier=None, words=None, weight=None):
        self.dict_specifier = dict_specifier
        self.words = []
        self.removed_words = []
        self._i = 0
        if isinstance(dict_specifier, (list, np.ndarray)):
            self.add(dict_specifier)
        if isinstance(dict_specifier, str):
            self.read(dict_specifier)
        if words is not None:
            self.add(words, weight)

    def __sizeof__(self):
        return sys.getsizeof(self.words) + sys.getsizeof(self.removed_words)

    @property
    def size(self):
        return len(self.words)

    @property
    def weight(self):
        return list(map(lambda x: x.weight, self.words))

    @property
    def w_len(self):
        return list(map(len, self.words))

    def __getitem__(self, key):
        return {'word': self.words[key], 'weight': self.words[key].weight, 'len': self.w_len[key]}

    def __repr__(self):
        return str({"words": self.words, "weight": self.weight})

    def __str__(self):
        return str({"words": self.words, "weight": self.weight})

    def __len__(self):
        return self.size

    def __add__(self, other):
        new_dict = copy.deepcopy(self)
        if isinstance(other, Dictionary):
            for wo, we in other:
                new_dict.add(wo, we)
        if isinstance(other, str):
            new_dict.add(other, 0)
        if isinstance(other, (tuple, list)):
            new_dict.add(other[0], other[1])
        if isinstance(other, dict):
            new_dict.add(other["word"], other["weight"])
        return new_dict

    def __sub__(self, other):
        new_dict = copy.deepcopy(self)
        if isinstance(other, Dictionary):
            for wo in other:
                new_dict.remove(wo)
        if isinstance(other, str):
            new_dict.remove(other)
        if isinstance(other, list):
            new_dict.remove(other)
        return new_dict

    def __iter__(self):
        return self

    def __next__(self):
        if self._i == self.size:
            self._i = 0
            raise StopIteration()
        word = self.words[self._i]
        self._i += 1
        return word, word.weight

    def get_k(self, word):
        return np.where(self.words == word)[0][0]

    def include(self, word):
        return word in self.words

    def add(self, words=None, weight=None, dict_specifier=None):
        if words is None and dict_specifier is None:
            raise ValueError("'words' or 'dict_specifier' must be specified")
        if words is dict_specifier is not None:
            raise ValueError("'words' or 'dict_specifier' must be specified")
        if dict_specifier is not None:
            self.read(dict_specifier)
        if words is not None:
            if isinstance(words, str):
                words = [words]
            if weight is None:
                weight = [0]*len(words)
            if isinstance(weight, (int, float)):
                weight = [weight]
            if len(words) != len(weight):
                raise ValueError(f"'words' and 'weight' must be same size")
            for wo, we in zip(words, weight):
                wo = wo.strip()
                if self.include(wo): # replace the weight
                    self.words[self.words.index(wo)].weight = we
                else:
                    self.words.append(Word(wo, we))

    def remove(self, words=None):
        if words is None:
            raise ValueError("'words' must be specified")
        if isinstance(words, str):
            words = [words]
        for wo in words:
            if self.include(wo):
                index = self.words.index(wo)
                del self.words[index]
                del self.weight[index]

    def read(self, dict_specifier):
        with open(dict_specifier, 'r', encoding='utf-8-sig') as f:
            data = f.read().splitlines()
        data = [l for l in data if l != ""]
        def get_word_and_weight(line):
            wo_we = line.split(" ")
            if len(wo_we) == 1:
                return wo_we[0], 0
            return wo_we[0], int(wo_we[1])

        dic_list = list(map(get_word_and_weight, data))
        word = [d[0] for d in dic_list]
        weight = [d[1] for d in dic_list]
        self.add(word, weight)

    def delete_unusable_words(self):
        """
        This method checks words in the dictionary and erases words that can not cross any other words.
        """
        merged_words = "".join(self.words)
        counts = collections.Counter(merged_words)
        for i, w in enumerate(self.words[:]):
            char_value = 0
            for char in set(w):
                char_value += counts[char]
            if char_value == len(w):
                self.removed_words.append(w)
                del self.words[i]

    def calc_weight(self):
        """
        Calculate word weights in the dictionary.
        """
        merged_words = "".join(self.words)
        counts = collections.Counter(merged_words)

        for i, w in enumerate(self.words):
            for char in w:
                self.words[i].weight += counts[char]
