# coding: utf-8
# In[]
import sys
import numpy as np

sys.path.append("../")
from pyzzle import Puzzle, FancyPuzzle, Dictionary, ObjectiveFunction, Optimizer

# In[]
# Set variables
dict_path = "../dict/pokemon.txt"  # countries hokkaido animals kotowaza birds dinosaurs fishes sports
width = 15
height = 15
with_weight = False

seed = 1
np.random.seed(seed=seed)

# In[]
## Make instances
### FuncyPuzzle
mask = np.array([
    [0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],
    [0,0,0,1,1,1,1,1,1,1,1,1,0,0,0],
    [0,0,1,1,1,1,1,1,1,1,1,1,1,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [1,1,1,1,1,1,0,0,0,1,1,1,1,1,1],
    [1,1,1,1,1,0,0,0,0,0,1,1,1,1,1],
    [1,1,1,1,1,0,0,0,0,0,1,1,1,1,1],
    [1,1,1,1,1,0,0,0,0,0,1,1,1,1,1],
    [1,1,1,1,1,1,0,0,0,1,1,1,1,1,1],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,0,1,1,1,1,1,1,1,1,1,1,1,0,0],
    [0,0,0,1,1,1,1,1,1,1,1,1,0,0,0],
    [0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],
], dtype="bool")
puzzle = FancyPuzzle(mask, "ドーナツパズル")

### Puzzle (normal)
# puzzle = Puzzle(width, height)

### Dictionary, ObjectiveFunction, Optimizer
dic = Dictionary(dict_path)
obj_func = ObjectiveFunction()
optimizer = Optimizer()

# In[]
puzzle.import_dict(dic)
# Register and set method and compile
obj_func.register(
    ["weight",
    "nwords", 
    "cross_count", 
    "fill_count", 
    "max_connected_empties", 
    "difficulty"]
    )
optimizer.set_method("local_search")
puzzle.compile(obj_func=obj_func, optimizer=optimizer)

# In[]
puzzle.first_solve()

# In[]
puzzle.solve(epoch=3)
print(f"unique solution: {puzzle.is_unique}")

# In[]
print(puzzle.cell)
print(f"単語リスト：{puzzle.used_words[:puzzle.nwords]}")
oname = f"{dic.name}_w{width}_h{height}_r{seed}.png"
puzzle.save_answer_image(f"fig/answer_{oname}")
puzzle.save_problem_image(f"fig/problem_{oname}")
print(f"Save as '{oname}'")

puzzle.export_json(f"json/{dic.name}_w{width}_h{height}_r{seed}.json")

# In[]
puzzle.show_log()

# In[]
