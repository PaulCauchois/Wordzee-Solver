from matplotlib import pyplot as plt
import os
import pickle


def end_numbers(string):
    r = ""
    for c in string[::-1]:
        if c in "123456789.":
            r += c
        else:
            break
    return r[::-1]


try:
    with open("Simulations.picl", 'rb') as f:
        simuls = pickle.load(f)
except (FileNotFoundError, EOFError):
    simuls = {}
    with open("Simulations.picl", 'wb+') as f:
        pickle.dump(simuls, f)

num_params = 2
bin_length = 5
max_score = 1200
plot_method = "KPPV_search"
logdir = "D://Wordzee/logs/" + plot_method
points = []
bins = range(bin_length // 2, max_score, bin_length)
bin_heights = [0 for _ in bins]
for file in os.listdir(logdir):
    if (filename := file[:-4]) in simuls:
        p = simuls[filename]["points"]
        points.append(simuls[filename])
        bin_heights[simuls[filename] // bin_length] += 1
    elif file.startswith(plot_method):
        if filename.endswith("000"):
            print(filename)
        with open(os.path.join(logdir, file), 'r') as f:
            r = f.readlines()
            V = {}
            end_of_params = list(map(lambda x: x[0], r)).index('b')
            for k in range(1, end_of_params):
                V["param" + str(k)] = end_numbers(r[k].strip('\n'))
            try:
                p = int(r[-1][13:])
                w = eval(r[-2][-6:-1])
            except (ValueError, NameError, IndexError):
                print(f"Invalid value encountered in {file}, moving on...")
            else:
                points.append(p)
                bin_heights[p // bin_length] += 1
                V["points"] = p
                V["wordzee"] = w
            simuls[filename] = V

with open("Simulations.picl", "wb+") as f:
    pickle.dump(simuls, f)
n = sum(bin_heights) * bin_length
freqs = [x / n for x in bin_heights]

plt.plot(bins, freqs)
plt.legend(["KPPV"])
plt.title("Comparison of solving methods")
plt.ylim((0, max(freqs)))
plt.show()
