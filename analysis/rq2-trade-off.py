import numpy as np
from scipy import stats
import seaborn as sb
import matplotlib.pyplot as plt


pkg = []
ram = []
gpu = []
tim = []
pre = []

name = []
p_values = []
power = {}
all_power = []


# read txt to list above
def read(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as file:
        # 0: power; 1: para; 2: \n
        line_cnt = 0
        for line in file.readlines():
            if "$end$" in line:
                break
            if line_cnt % 3 == 0:
                str_buf = ""
                cnt = 0
                pkg_buf = 0.0
                ram_buf = 0.0
                gpu_buf = 0.0
                tim_buf = 0.0
                pre_buf = 0.0
                for char in line:
                    if char.isdigit() or char ==".":
                        str_buf = str_buf + char
                    else:
                        if len(str_buf):
                            if cnt < 5:
                                pkg_buf += float(str_buf)
                            elif cnt < 10:
                                ram_buf += float(str_buf)
                            elif cnt < 15:
                                tim_buf += float(str_buf)
                            elif cnt < 20:
                                gpu_buf += float(str_buf)
                            else:
                                pre_buf += float(str_buf)
                            cnt += 1
                        str_buf = ""
            elif line_cnt % 3 == 1:
                # read file name
                s = line.split(" ")
                name.append(s[0])
                # read p values
                buf = {}
                buf["pkg"] = int(s[2][0])
                buf["ram"] = int(s[4][0])
                buf["tim"] = int(s[6][0])
                buf["gpu"] = int(s[8][0])
                buf["pre"] = int(s[10][0])
                p_values.append(buf)
            else:
                pkg.append(pkg_buf / 5)
                ram.append(ram_buf / 5)
                gpu.append(gpu_buf / 5)
                tim.append(tim_buf / 5)
                pre.append(pre_buf / 5)
            line_cnt += 1


def display():
    print(name)
    print(p_values)
    print(power)
    # print(pkg)
    # print(ram)
    # print(gpu)
    # print(tim)
    # print(pre)


# init_power
def init():
    power["pkg"] = pkg
    power["ram"] = ram
    power["gpu"] = gpu
    power["tim"] = tim
    power["pre"] = pre
    for i in range(16):
        all_power.append(pkg[i] + ram[i] + gpu[i])


# generate table
def table1():
    res = []
    keys = ["pkg", "ram", "gpu", "tim", "pre"]
    for i in range(16):
        buf = {}
        # name
        buf["name"] = name[i]
        # pkg
        for k in keys:
            if p_values[i][k] == 1:
                buf[k] = 0
            else:
                if power[k][i] > power[k][0]:
                    buf[k] = 1
                elif power[k][i] < power[k][0]:
                    buf[k] = -1
                # error
                else:
                    buf[k] = 2
        # output
        # ouput_s(buf)
        res.append(buf)
    return res


# all 9 table
#     pkg    ram     gpu
# E   3*3
# L
# x
def table2(data):
    # print(data)
    all_wtl = []

    # 3*3
    # 1/-1     1/0    1/1
    # 0/-1     0/0    0/1
    # -1/-1   -1/0   -1/1

    # epoch
    pkg_buf = [[0 for j in range(3)]for i in range(3)]
    ram_buf = [[0 for j in range(3)]for i in range(3)]
    gpu_buf = [[0 for j in range(3)]for i in range(3)]
    for i in range(1, 6):
        pkg_buf[1 - data[i]["pkg"]][data[i]["pre"] + 1] += 1
        ram_buf[1 - data[i]["ram"]][data[i]["pre"] + 1] += 1
        gpu_buf[1 - data[i]["gpu"]][data[i]["pre"] + 1] += 1
    all_wtl.append(pkg_buf)
    all_wtl.append(ram_buf)
    all_wtl.append(gpu_buf)

    # lr
    pkg_buf = [[0 for j in range(3)] for i in range(3)]
    ram_buf = [[0 for j in range(3)] for i in range(3)]
    gpu_buf = [[0 for j in range(3)] for i in range(3)]
    for i in range(6, 11):
        pkg_buf[1 - data[i]["pkg"]][data[i]["pre"] + 1] += 1
        ram_buf[1 - data[i]["ram"]][data[i]["pre"] + 1] += 1
        gpu_buf[1 - data[i]["gpu"]][data[i]["pre"] + 1] += 1
    all_wtl.append(pkg_buf)
    all_wtl.append(ram_buf)
    all_wtl.append(gpu_buf)

    # lr
    pkg_buf = [[0 for j in range(3)] for i in range(3)]
    ram_buf = [[0 for j in range(3)] for i in range(3)]
    gpu_buf = [[0 for j in range(3)] for i in range(3)]
    for i in range(11, 16):
        pkg_buf[1 - data[i]["pkg"]][data[i]["pre"] + 1] += 1
        ram_buf[1 - data[i]["ram"]][data[i]["pre"] + 1] += 1
        gpu_buf[1 - data[i]["gpu"]][data[i]["pre"] + 1] += 1
    all_wtl.append(pkg_buf)
    all_wtl.append(ram_buf)
    all_wtl.append(gpu_buf)

    # print(all_wtl)
    return all_wtl


def plot_hm(name, wtl):
    # print(wtl)
    ec = ["package", "ram", "gpu"]
    for i in range(3):
        for j in range(3):
            xl = ["loss", "tie", "win"]
            yl = ["win", "tie", "loss"]
            # print(wtl[i])
            data = np.array((wtl[3 * i + j]))
            # print(data)
            font_text = {'family': 'Times New Roman',
                         'weight': 'bold',  # 字体加速
                         'color': 'black',
                         'size': 45,
                         }
            plt.figure(figsize=(10, 8))
            plt.gcf().subplots_adjust(bottom=0.16)
            sb.set(context='notebook', style='ticks', font_scale=3)
            hm = sb.heatmap(data, annot=True, xticklabels=xl,
                            yticklabels=yl)
            plt.tick_params(labelsize=40)
            plt.xlabel("performance", font_text)
            plt.ylabel(ec[j] + " energy consumption", font_text)
            # plt.title(title[i] + "-" + ec[j])
            plt.show()


def ouput_s(buf):
    keys = ["pkg", "ram", "gpu", "tim", "pre"]
    s = buf["name"]
    for k in keys:
        s = s + "\t" + k + ": " + str(buf[k])
    print(s)


def all_clear():
    pkg.clear()
    ram.clear()
    gpu.clear()
    tim.clear()
    pre.clear()
    name.clear()
    p_values.clear()
    power.clear()
    all_power.clear()


# test
# p = "mff"
# read(p + ".txt")
# init()
#
# matrix = table2(table1())
# plot_hm(p, matrix)

# all p value
paths = ["mnist_new", "mff", "sia", "resnet", "hr18"]
# paths = ["mnist_new", "mff", "mnist_new", "sia", "sia", "mff", "sia", "mnist_new"]
# paths = ["mff"]
total_wtl = [[[0 for j in range(3)]for i in range(3)] for k in range(9)]

for p in paths:
    read(p + ".txt")
    init()
    # display()
    # plot_hm(p, table2(table1()))
    print(table1())
    single_wtl = table2(table1())
    # print(single_wtl)
    for i in range(9):
        for j in range(3):
            for k in range(3):
                total_wtl[i][j][k] += single_wtl[i][j][k]
    all_clear()

print(total_wtl)
# plot_hm("total", total_wtl)

# rq3
# paths = ["mst/mff", "mst/sia", "sia/mff", "sia/mst"]
paths = ["mst/mff"]
rq3_wtl = [[[0 for j in range(3)]for i in range(3)] for k in range(9)]
for p in paths:
    read("comp/" + p + ".txt")
    init()
    # display()
    single_wtl = table2(table1())
    # print(single_wtl)
    for i in range(9):
        for j in range(3):
            for k in range(3):
                rq3_wtl[i][j][k] += single_wtl[i][j][k]
    # print(single_wtl)
    all_clear()

print(rq3_wtl)
# for i in range(9):
#     for j in range(3):
#         for k in range(3):
#             rq3_wtl[i][j][k] -= total_wtl[i][j][k]
# print(rq3_wtl)
# plot_hm("rq3", rq3_wtl)
