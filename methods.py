from collections import Counter
import random
import itertools

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

Alphabet = list(scores.keys())


def powerset(s):
    return set([x for k in range(len(s) + 1) for x in itertools.combinations(s, k)])


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


def words_containing(string, words, scoring=None):
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


def swap_letters(kept, n):
    return list(kept) + list(random.choice(Alphabet) for _ in range(n - len(kept)))


def probabilistic_search(initials, cases, words, num_tries):
    n = len(initials)
    roots = list(powerset(initials))
    averages = {str(initials): max(words_containing(initials, words, cases).values())}
    tests = 0
    for root in roots:
        averages[root] = 0
        for _ in range(num_tries):
            new_letters = swap_letters(root, n)
            averages[root] += max(words_containing(new_letters, words, cases).values())
            tests += 1
        averages[root] /= num_tries

    best = max(roots, key=lambda x: averages[x])

    return best


def exhaustive_search(initials, cases, words, max_swaps):
    n = len(initials)
    roots = []
    averages = {}
    tested = {}

    for k in range(1, max_swaps + 1):
        for root in itertools.combinations(initials, n - k):
            roots.append(root)

    roots = [*set(roots)]
    averages[str(initials)] = max(words_containing(initials, words, cases).values())
    for root in roots:
        s = 0
        k = n - len(root)
        for added in itertools.product(list(scores.keys()), repeat=k):
            new_string = str(sorted(root + added))
            if new_string in tested:
                s += tested[new_string]
            else:
                b = max(words_containing(new_string, words, cases).values())
                s += b
                tested[new_string] = b
        averages[root] = s / (26 ** k)

    best = max(roots, key=lambda x: averages[x])

    return best


def KPPV_search(initials, cases, words, k, seuil):
    results = words_containing(initials, words, cases)
    l = min(len(results), k)
    filtered = sorted(results.keys(), key=results.get, reverse=True)[:l]
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

    return kept
