import math
import random
import itertools
from collections import defaultdict
from copy import deepcopy

# non-repetitive n digits number generator
def generate_number(n):
    digits = list(range(10))
    random.shuffle(digits)
    return tuple(digits[:n])

# A : correct number, correct position 
# B : correct number, wrong position
def generate_clue(x, ans):
    A = B = 0
    for num_1, num_2 in zip(x, ans):
        if num_1 == num_2:
            A += 1
        elif num_1 in ans:
            B += 1
    clue = (1 + len(ans)) * A + B
    return clue

# generate lookup table
def generate_table(n):
    perm = list(itertools.permutations(range(10), n))
    table = defaultdict(set)
    for n1, n2 in itertools.combinations_with_replacement(perm, 2):
        clue = generate_clue(n1, n2)
        table[(n1, clue)].add(n2)
        table[(n2, clue)].add(n1)
    return table

# generate entropy
def calculate_entropy(guess, table):
    n = len(guess)
    counts = [0] * (n**2 + n + 1)
    for m in range(n**2 + n + 1):
        counts[m] = len(table[(guess, m)])
    total = sum(counts)
    if total == 0:
        return math.inf
    ps = [c / total for c in counts]
    entropy = sum([-p * math.log(p, 2) for p in ps if p != 0])
    return entropy

# alter table based on x, m
def alter_table(x, m, table):
    for key in table.keys():
        table[key] &= table[(x, m)]

# guess
def guess(table, candids):
    if len(candids) == 1:
        return candids.pop()
    # all permutations
    perms = set(perm for perm, m in table.keys())
    # entropy
    items = [(calculate_entropy(perm, table), int(perm in candids), perm) for perm in perms]
    items.sort(reverse=True)
    guess = items[0][-1]
    return guess


def round(dim, table_ori):
    # generate answer
    ans = generate_number(dim)
    print("Ans : ", ans)
    # init
    i = 0
    table = deepcopy(table_ori)
    candids = list(itertools.permutations(range(10), dim))
    # start guessing
    while True:
        i += 1
        x = guess(table, candids)
        m = generate_clue(x, ans)
        candids = table[(x, m)]
        # update table
        alter_table(x, m, table)
        A, B = divmod(m, dim + 1)
        print("Guess %d: %s, %dA%dB ; candids: %d" % (i, x, A, B, len(candids)))
        if m == (dim + 1) * dim:
            break

def main(dim):
    # prime table
    table_ori = generate_table(dim)
    for i in range(100):
        print("")
        print("Round %d" % (i + 1))
        round(dim, table_ori)

if __name__ == "__main__":
    dim = 4
    main(dim)