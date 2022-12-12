from matplotlib import pyplot as plt
import os

num_params = 2
plot_method = "KPPV_search"
logdir = os.getcwd() + "/logs/" + plot_method
points = []
for file in os.listdir(logdir):
    if file.startswith(plot_method):
        f = open(os.path.join(logdir, file), 'r')
        r = f.readlines()
        try:
            points.append(int(r[-1][13:]))
            if points[-1] > 900 :
                print(file)
        except ValueError:
            print(f"Invalid value encountered in {file}, moving on...")
        except IndexError:
            print(f"Invalid value encountered in {file}, moving on...")

param1 = int(r[1][4:])
if num_params == 2:
    param2 = float(r[2][8:])

plt.hist(points, bins=range(0, 1000, 10), density=True)
plt.show()
