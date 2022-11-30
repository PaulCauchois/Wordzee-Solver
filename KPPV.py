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
k = 10
seuil = 0.5

results = words_containing(initials, cases)
l = min(len(results), k)
filtered = sorted(results.keys(), key=results.get, reverse=True)[:l]
print(filtered)
total = sum([results[w] for w in filtered])
kept = []
if total:
    for i, c in enumerate(initials):
        s = 0
        for word in filtered:
            if Counter(initials[:i])[c] + 1 <= Counter(word)[c]:
                s += results[word]
        if s / total >= seuil:
            kept.append(c)

print(f"Keep letters {kept}")
new_string = input("New letters (lowercase) : ")
new_words = words_containing(new_string, cases)
b = max(new_words.values())

print(f"Best possible is/are {[i for i in new_words if new_words[i] == b]} with value {b}.")
