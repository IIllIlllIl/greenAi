import argparse
import math
import csv
import os

import numpy as np
from scipy import stats
from cliffs_delta import cliffs_delta

data_num = 5


def to_float(str):
    value = 0
    splited_str = str.split(",")
    size = len(splited_str)
    for piece in splited_str:
        value += float(piece) * math.pow(1000, size - 1)
        size -= 1
    return value


def read_data(path):
    data = []

    cpu_data = open(path + "/cpu.log", 'r')
    try:
        while True:
            line = cpu_data.readline()
            if line:
                if "power/energy-pkg/" in line or "power/energy-ram/" in line or "time" in line:
                    power_line = line.split(" ")
                    for power in power_line:
                        if '.' in power:
                            data.append(to_float(power))
            else:
                break
    finally:
        cpu_data.close()

    nvidia_data = open(path + "/nvidia_smi1.log", 'r')
    try:
        cnt = 0
        power = 0
        cntList = [0,1,2,3,4,5,6,7]
        while True:
            line = nvidia_data.readline()
            if line:
                if cnt % 8 in cntList:
                    power += float(line.split(' W,')[0])
                cnt += 1
            else:
                break
        if cnt != 0:
            data.append(power)
    finally:
        nvidia_data.close()

    pre_data = open(path + "/out.log", 'r')
    try:
        pre = "0"
        while True:
            line = pre_data.readline()
            if line:
                if 'test acc' in line:
                    pre = float(line.split(" ")[2])
            else:
                break
        data.append(pre)
    finally:
        pre_data.close()
    return data


def p_value(arrA, arrB):
    a = np.array(arrA)
    b = np.array(arrB)

    t, p = stats.ttest_ind(a, b)

    return p


def read(file_name):
    energy = {"pkg": [], "ram": [], "tim": [], "gpu": [], "pre": []}
    path = "./mnist/" + file_name + "/" + file_name + "-"
    for i in range(data_num):
        si = str(i)
        file_path = path + si
        file_list = read_data(file_path)
        energy["pkg"].append(file_list[0])
        energy["ram"].append(file_list[1])
        energy["tim"].append(file_list[2])
        energy["gpu"].append(file_list[3])
        energy["pre"].append(file_list[4])
    return energy


def evaluate_single(key, mut, ori):
    print(key + ":")
    p = p_value(mut[key], ori[key])
    print("p-value: " + str(p))
    delta = cliffs_delta(mut[key], ori[key])
    print("cliffs delta: " + str(delta))
    return [p, delta]


def evaluate(mut, ori):
    result = {"pkg": evaluate_single("pkg", mut, ori), "ram": evaluate_single("ram", mut, ori),
              "tim": evaluate_single("tim", mut, ori),
              "gpu": evaluate_single("gpu", mut, ori), "pre": evaluate_single("pre", mut, ori)}
    return result


def collect(file):
    os.system("mkdir " + file)
    for i in range(data_num):
        si = str(i)
        mv_cmd = "mv " + file + "-" + si + " " +file
        # print(mv_cmd)
        os.system(mv_cmd)
    os.system("mv " + file + " mnist")
    os.system("rm -r " + file)


def same_single(key, mut, ori):
    flag = -1
    p = p_value(mut[key], ori[key])
    delta = cliffs_delta(mut[key], ori[key])
    if p > 0.05 or -0.147 < delta[0] < 0.147:
        flag = 1
    else:
        flag = 0
    return flag


def same(mut, ori):
    result = {"pkg": same_single("pkg", mut, ori), "ram": same_single("ram", mut, ori),
              "tim": same_single("tim", mut, ori),
              "gpu": same_single("gpu", mut, ori), "pre": same_single("pre", mut, ori)}
    return result


def same_csv(file, mut, ori, path):
    with open(path, mode='a') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([file, same_single("pkg", mut, ori), same_single("ram", mut, ori),
                        same_single("tim", mut, ori),
                        same_single("gpu", mut, ori), same_single("pre", mut, ori)])
        csv_file.close()


parser = argparse.ArgumentParser()
parser.add_argument('-k', '--key', default="NA", type=str)
parser.add_argument('-d', '--dir', default="NA", type=str)
parser.add_argument('-n', '--name', default="NA", type=str)
parser.add_argument('-c', '--collect', default="NA", type=str)
args = parser.parse_args()

name = args.name

#origin = read("p")

if name != "NA":
    mutant = read(name)
    print(mutant)
    # evaluate(mutant, origin)
    origin = read("p")
    print(name + " " + str(same(mutant, origin)))
elif args.collect != "NA":
    collect(args.collect)
elif args.key == "evaluate":
    path = "./data.csv"
    os.system("rm " + path)
    origin = read("p")
    for n in os.listdir("./mnist"):
        if n != 'p':
            print(n)
            mutant = read(n)
            evaluate(mutant, origin)
elif args.key == "csv":
    path = "./data.csv"
    os.system("rm " + path)
    origin = read("p")
    for n in os.listdir("./mnsit"):
        if n != 'p':
            print(n)
            mutant = read(n)
            same_csv(n, mutant, origin, path)

