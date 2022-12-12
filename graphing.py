from matplotlib import pyplot as plt
import os

logdir = os.getcwd() + "/logs"
num_params = 2
plot_method = "KPPV_search"
points = []
for file in os.listdir(logdir):
    if file.startswith(plot_method):
        f = open(os.path.join(logdir, file), 'r')
        r = f.readlines()
        points.append(int(r[-1][13:]))

param1 = int(r[1][4:])
if num_params == 2:
    param2 = float(r[2][8:])

plt.hist(points, bins=range(0, 1000, 10), density=True)
plt.show()
