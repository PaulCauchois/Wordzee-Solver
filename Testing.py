import random
from methods import *


def create_game():
    bonuses = ['LD', 'LD', 'LD', 'LT', 'LT']
    random.shuffle(bonuses)
    board = []
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
        board.append(row)
    return board


def play_game(method, param1, param2=None):
    board = create_game()
    plays = []
    points = 0
    wordzee = True
    for row in board:
        print(f"Playing round {row}")
        k = len(row)
        letters = swap_letters('', 7)
        print(f"Letters are {letters}")
        for _ in range(2):
            if param2:
                kept = method(letters, row, words, param1, param2)
            else:
                kept = method(letters, row, words, param1)
            print(f"Keeping {kept}")
            letters = swap_letters(kept,7)
            print(f"New letters are {letters}")
        P = words_containing(letters, words, row)
        played = max(P.keys(), key=P.get)
        print(f"Playing {played} for {P[played]} points")
        points += P[played]
        if len(played) < k:
            wordzee = False
            plays.append(list(played) + (k - len(played)) * [''])
        else:
            plays.append(list(played))
        print("-----------")
    if wordzee:
        points += 100
        print("Wordzee !")
    return plays, points


words = {}
f = open("French ODS dictionary.txt")
for line in iter(f.readline, ''):
    if len(line) in (4, 5, 6, 7, 8):
        lw = line[:-1].lower()
        words[lw] = Counter(lw)

A,B = play_game(exhaustive_search,3)

print(A)
print(B)