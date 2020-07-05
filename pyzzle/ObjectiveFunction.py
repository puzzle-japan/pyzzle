import numpy as np
from scipy import ndimage


class ObjectiveFunction:
    flist = [
        "weight",
        "nwords",
        "cross_count",
        "cross_rate",
        "fill_count",
        "max_connected_empties",
        "difficulty",
        "ease",
        "circulation",
        "gravity",
    ]

    def __init__(self, objective_function=["nwords"]):
        if not isinstance(objective_function, (list, tuple, set)):
            raise TypeError("'objective_function' must be list or tuple or set")
        self.register(objective_function)

    def __len__(self):
        return len(self.registered_funcs)

    def get_funcs(self):
        return self.registered_funcs

    @classmethod
    def nwords(self, puzzle):
        """
        This method returns the number of words used in the solution.
        """
        return puzzle.nwords

    @classmethod
    def cross_count(self, puzzle):
        """
        This method returns the number of crosses of a word.
        """
        return np.sum(puzzle.cover == 2)

    @classmethod
    def cross_rate(self, puzzle):
        """
        This method returns the rate of crosses of a word.
        """
        return ObjectiveFunction.cross_count(puzzle)/ObjectiveFunction.nwords(puzzle)

    @classmethod
    def fill_count(self, puzzle):
        """
        This method returns the number of character cells in the puzzle.
        """
        return np.sum(puzzle.cover >= 1)

    @classmethod
    def weight(self, puzzle):
        """
        This method returns the sum of the word weights used for the solution.
        """
        return puzzle.weight

    @classmethod
    def max_connected_empties(self, puzzle):
        """
        This method returns the maximum number of concatenations for unfilled squares.
        """
        reverse_cover = puzzle.cover < 1
        zero_label, n_label = ndimage.label(reverse_cover)
        mask = zero_label > 0
        sizes = ndimage.sum(mask, zero_label, range(n_label+1))
        score = puzzle.width*puzzle.height - sizes.max()
        return score

    @classmethod
    def difficulty(self, puzzle):
        return puzzle.difficulty

    @classmethod
    def ease(self, puzzle):
        return 1 - puzzle.difficulty

    @classmethod
    def circulation(self, puzzle):
        return puzzle.circulation

    @classmethod
    def gravity(self, puzzle):
        return puzzle.gravity[puzzle.cover != 0].sum()

    def register(self, func_names):
        """
        This method registers an objective function in an instance
        """
        for func_name in func_names:
            if func_name not in self.flist:
                raise RuntimeError(f"ObjectiveFunction class does not have '{func_name}' function")
        self.registered_funcs = func_names

    def get_score(self, puzzle, i=0, func=None, all=False):
        """
        This method returns any objective function value
        """
        if all is True:
            scores = {}
            # scores = np.zeros(len(self.registered_funcs), dtype="float")
            for func_name in self.registered_funcs:
                scores[func_name] = eval(f"self.{func_name}(puzzle)")
            return scores
        if func is None:
            func = self.registered_funcs[i]
        return eval(f"self.{func}(puzzle)")
