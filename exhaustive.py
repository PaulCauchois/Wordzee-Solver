from collections import Counter
import itertools
import time

Alphabet = "azertyuiopqsdfghjklmwxcvbn"

scores = {'a': 1,
          'b': 3,
          'c': 3,
          'd': 2,
          'e': 1,
          'f': 4,
          'g': 2,
          'h': 4,
          'i': 1,
          'j': 8,
          'k': 10,
          'l': 1,
          'm': 2,
          'n': 1,
          'o': 1,
          'p': 3,
          'q': 8,
          'r': 1,
          's': 1,
          't': 1,
          'u': 1,
          'v': 4,
          'w': 10,
          'x': 10,
          'y': 10,
          'z': 10
          }


def score(word, scoring=None):
    s = 0
    if scoring is None:
        for c in word:
            s += scores[c]
    else:
        product = 1
        for c, m in zip(word, scoring):
            match m:
                case 'LD':
                    s += scores[c] * 2
                case 'LT':
                    s += scores[c] * 3
                case 'MD':
                    product *= 2
                    s += scores[c]
                case 'MT':
                    product *= 3
                    s += scores[c]
                case _:
                    s += scores[c]
        s *= product
        if len(word) == len(scoring):
            s += 20
    return s


def words_containing(string, scoring=None):
    l = {'': 0}
    C = Counter(string)
    if scoring:
        for w in words:
            if len(w) <= len(scoring) and words[w] <= C:
                l[w] = score(w, scoring)
    else:
        for w in words:
            if words[w] <= C:
                l[w] = score(w)
    return l


words = {}
f = open("French ODS dictionary.txt")
for line in iter(f.readline, ''):
    if len(line) in (4, 5, 6, 7, 8):
        lw = line[:-1].lower()
        words[lw] = Counter(lw)

initials = sorted("azertyu")
cases = ['LD', '', '', '', '', '', 'MT']
n = len(initials)
max_swaps = 2

roots = []
averages = {}
tested = {}
for k in range(1, max_swaps + 1):
    for root in itertools.combinations(initials, n - k):
        roots.append(root)

roots = [*set(roots)]
averages[str(initials)] = max(words_containing(initials, cases).values())
start_time = time.time()
for root in roots:
    print("___________")
    print(f"Processing root {root} :")
    s = 0
    k = n - len(root)
    for added in itertools.product(Alphabet, repeat=k):
        new_string = str(sorted(root + added))
        if new_string in tested:
            s += tested[new_string]
        else:
            b = max(words_containing(new_string, cases).values())
            s += b
            tested[new_string] = b
    averages[root] = s / (26 ** k)
    print(f"Average for root {root} is {averages[root]}")

print("__________")
best = max(roots, key=lambda x: averages[x])
print(f"{len(tested)} values computed in {time.time() - start_time} seconds.")
print(f"Overall best is {best} with average {averages[best]}")

new_string = input("New letters (lowercase) : ")
new_words = words_containing(new_string, cases)
b = max(new_words.values())

print(f"Best possible is/are {[i for i in new_words if new_words[i] == b]} with value {b}.")
