from matplotlib import pyplot as plt
from collections import Counter

f = open("letters.txt")
letters = Counter("")
for l in iter(f.readline, ''):
    letters += Counter(l[:-1])

n = sum(letters.values())
a, b = [], []
for x in letters.most_common():
    a.append(x[0])
    b.append(x[1] / n)

plt.bar(a, b)
plt.show()
