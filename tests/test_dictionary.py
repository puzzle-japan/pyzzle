import unittest
from pathlib import PurePath

from pyzzle import Dictionary


class TestDictionary(unittest.TestCase):
    """Test the Dictionary class."""

    def test_add(self):
        d = Dictionary()
        d += "word1"
        d += ["word2", 1]
        self.assertEqual(["word1", "word2"], d.words)
        self.assertEqual([0, 1], d.weight)

    def test_add_with_dictionary(self):
        d = Dictionary(words="word1")
        d += Dictionary(words="word2", weight=1)
        self.assertEqual(["word1", "word2"], d.words)
        self.assertEqual([0, 1], d.weight)

    def test_add_word(self):
        d = Dictionary()
        d.add("word1")
        d.add("word2", 1)
        self.assertEqual(["word1", "word2"], d.words)
        self.assertEqual([0, 1], d.weight)

    def test_add_multiple_words(self):
        d = Dictionary()
        d.add(["word1", "word2", "word3"], [0, 1, 2])
        self.assertEqual(["word1", "word2", "word3"], d.words)
        self.assertEqual([0, 1, 2], d.weight)

    def test_add_duplicated_word(self):
        d = Dictionary()
        d.add("word1", 0)
        d.add("word1", 1)
        self.assertEqual(["word1"], d.words)
        self.assertEqual([1], d.weight)

    def test_sub(self):
        d = Dictionary()
        d.add(["word1", "word2"])
        d -= "word1"
        self.assertEqual(["word2"], d.words)
        self.assertEqual([0], d.weight)

    def test_sub_with_dictionary(self):
        d = Dictionary(words=["word1", "word2", "word3"])
        d -= Dictionary(words=["word1", "word2"])
        self.assertEqual(["word3"], d.words)
        self.assertEqual([0], d.weight)

    def test_remove_word(self):
        d = Dictionary()
        d.add(["word1", "word2"])
        d.remove("word1")
        self.assertEqual(["word2"], d.words)
        self.assertEqual([0], d.weight)

    def test_remove_multiple_words(self):
        d = Dictionary()
        d.add(["word1", "word2", "word3"])
        d.remove(["word1", "word2"])
        self.assertEqual(["word3"], d.words)
        self.assertEqual([0], d.weight)

    def test_iter(self):
        d = Dictionary()
        d.add(["word1", "word2", "word3"], [0, 1, 2])
        words = []
        weights = []
        for wo, we in d:
            words.append(wo)
            weights.append(we)
        self.assertEqual(["word1", "word2", "word3"], words)
        self.assertEqual([0, 1, 2], weights)

    def test_size_property(self):
        d = Dictionary(words="word1")
        self.assertEqual(1, d.size)

    def test_w_len_property(self):
        d = Dictionary(words="word1")
        self.assertEqual([5], d.w_len)

    def test_delete_bom(self):
        dict_dir = str(PurePath(__file__).parent / PurePath("data"))
        d = Dictionary(f"{dict_dir}/dict_with_bom.txt")
        self.assertEqual(["word1", "word2"], d.words)
