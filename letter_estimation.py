from matplotlib import pyplot as plt
from collections import Counter
import math

f = open("letters.txt")
letters = Counter("")
for l in iter(f.readline, ''):
    letters += Counter(l[:-1])

n = sum(letters.values())
L, W = [], []
for x in letters.most_common():
    L.append(x[0])
    W.append(math.log(x[1] / n))

plt.bar(L, W)
plt.show()
