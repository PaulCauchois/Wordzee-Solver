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

logdir = "D://Wordzee/logs/"

for d in os.listdir(logdir):
    if os.path.isdir(logdir+d):
        for file in os.listdir(logdir+d):
            if os.path.isfile(file) and (filename := file[:-4]) not in simuls:
                with open(os.path.join(os.getcwd() + '/' + d + '/', file), 'r') as f:
                    r = f.readlines()
                    V = {}
                    entry_name = filename
                    end_of_params = list(map(lambda x: x[0], r)).index('b')
                    for k in range(1, end_of_params):
                        V["param" + str(k)] = end_numbers(r[k].strip('\n'))
                        entry_name += '|' + V["param" + str(k)]
                    try:
                        p = int(r[-1][13:])
                        w = eval(r[-2][-6:-1])
                    except (ValueError, NameError, IndexError):
                        print(f"Invalid value encountered in {file}, moving on...")
                    else:
                        V["points"] = p
                        V["wordzee"] = w
                    simuls[entry_name] = V

with open("Simulations.picl", "wb+") as f:
    pickle.dump(simuls, f)
