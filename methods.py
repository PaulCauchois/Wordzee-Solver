from collections import Counter
import random
import itertools


def powerset(s):
    return set([x for k in range(len(s) + 1) for x in itertools.combinations(s, k)])


class Wordzee:
    def __init__(self, wordfile, letterfile, board=None, scores=None):

        # Opening dictionary

        self.words = {}
        f = open(wordfile)
        for line in iter(f.readline, ''):
            if len(line) in (4, 5, 6, 7, 8):
                lw = line[:-1].lower()
                self.words[lw] = Counter(lw)

        # Opening random letters

        f = open(letterfile)
        letters = Counter("")
        for l in iter(f.readline, ''):
            letters += Counter(l[:-1])

        n = sum(letters.values())
        self.alphabet, self.probs = [], []
        for x in letters.most_common():
            self.alphabet.append(x[0])
            self.probs.append(x[1] / n)

        # Making board

        if board:
            self.board = board
        else:
            self.create_board()

        # Scores

        if scores:
            self.scores = scores
        else:
            self.scores = {'a': 1,
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

        self.max_letters = max([len(r) for r in self.board])
        self.letters = ''
        self.swap_letters('', inPlace=True)
        self.cases = self.board[0]
        # Bonus to make the algorithms prioritize filling up the row instead of simply going for points.
        # Has to be removed after computing the score, though.
        self.full_bonus = 100

    def create_board(self):
        bonuses = ['LD', 'LD', 'LD', 'LT', 'LT']
        random.shuffle(bonuses)
        self.board = []
        for i in range(3, 8):
            row = [bonuses[i - 3]] + ['' for _ in range(i - 2)]
            if i <= 5:
                row.append('')
                random.shuffle(row)
            elif i == 6:
                random.shuffle(row)
                row.append('MD')
            else:
                random.shuffle(row)
                row.append('MT')
            self.board.append(row)

    def score(self, word, scoring=None):
        s = 0
        if scoring is None:
            for c in word:
                s += self.scores[c]
        else:
            product = 1
            for c, m in zip(word, scoring):
                match m:
                    case 'LD':
                        s += self.scores[c] * 2
                    case 'LT':
                        s += self.scores[c] * 3
                    case 'MD':
                        product *= 2
                        s += self.scores[c]
                    case 'MT':
                        product *= 3
                        s += self.scores[c]
                    case _:
                        s += self.scores[c]
            s *= product
            if len(word) == len(scoring):
                s += self.full_bonus
        return s

    def words_containing(self, string, scoring=None):
        l = {'': 0}
        C = Counter(string)
        if scoring:
            for w in self.words:
                if len(w) <= len(scoring) and self.words[w] <= C:
                    l[w] = self.score(w, scoring)
        else:
            for w in self.words:
                if self.words[w] <= C:
                    l[w] = self.score(w)
        return l

    def swap_letters(self, kept, inPlace=True):
        if inPlace:
            self.letters = list(kept) + list(
                random.choices(self.alphabet, weights=self.probs, k=self.max_letters - len(kept)))
        else:
            return list(kept) + list(random.choices(self.alphabet, weights=self.probs, k=self.max_letters - len(kept)))

    def probabilistic_search(self, num_tries):
        roots = list(powerset(self.letters))
        averages = {str(self.letters): max(self.words_containing(self.letters, self.cases).values())}
        tests = 0
        for root in roots:
            averages[root] = 0
            for _ in range(num_tries):
                new_letters = self.swap_letters(root, False)
                averages[root] += max(self.words_containing(new_letters, self.cases).values())
                tests += 1
            averages[root] /= num_tries

        best = max(roots, key=lambda x: averages[x])

        return best

    def exhaustive_search(self, max_swaps):
        roots = []
        averages = {}
        tested = {}

        for k in range(1, max_swaps + 1):
            for root in itertools.combinations(self.letters, self.max_letters - k):
                roots.append(root)

        roots = [*set(roots)]
        averages[str(self.letters)] = max(self.words_containing(self.letters, self.cases).values())
        for root in roots:
            s = 0
            k = self.max_letters - len(root)
            for added in itertools.product(list(self.alphabet), repeat=k):
                new_string = str(sorted(root + added))
                if new_string in tested:
                    s += tested[new_string]
                else:
                    b = max(self.words_containing(new_string, self.cases).values())
                    s += b
                    tested[new_string] = b
            averages[root] = s / (26 ** k)

        best = max(roots, key=lambda x: averages[x])

        return best

    def KPPV_search(self, k, seuil):
        results = self.words_containing(self.letters, self.cases)
        l = min(len(results), k)
        filtered = sorted(results.keys(), key=results.get, reverse=True)[:l]
        total = sum([results[w] for w in filtered])
        kept = []
        if total:
            for i, c in enumerate(self.letters):
                s = 0
                for word in filtered:
                    if Counter(self.letters[:i])[c] + 1 <= Counter(word)[c]:
                        s += results[word]
                if s / total >= seuil:
                    kept.append(c)

        return kept
