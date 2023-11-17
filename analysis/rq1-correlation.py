import numpy as np
from scipy import stats
import seaborn as sb
import matplotlib.pyplot as plt


def p_value(arrA, arrB):
    a = np.array(arrA)
    b = np.array(arrB)

    t, p = stats.ttest_ind(a, b)

    return p


def pearson(arrA, arrB):
    a = np.array(arrA)
    b = np.array(arrB)

    t, p = stats.pearsonr(a, b)

    return t


def spearman(arrA, arrB):
    a = np.array(arrA)
    b = np.array(arrB)

    t, p = stats.spearmanr(a, b)

    return t


def p_pearson(arrA, arrB):
    a = np.array(arrA)
    b = np.array(arrB)

    t, p = stats.pearsonr(a, b)

    return p


def p_spearman(arrA, arrB):
    a = np.array(arrA)
    b = np.array(arrB)

    t, p = stats.spearmanr(a, b)

    return p


all_epoch = {"par": [], "pkg": [], "ram": [], "gpu": [], "tim": [], "pre": []}
all_lr = {"par": [], "pkg": [], "ram": [], "gpu": [], "tim": [], "pre": []}
all_gamma = {"par": [], "pkg": [], "ram": [], "gpu": [], "tim": [], "pre": []}
all_wd = {"par": [], "pkg": [], "ram": [], "gpu": [], "tim": [], "pre": []}

par = []
pkg = []
ram = []
gpu = []
tim = []
pre = []


# read txt to list above
def read(txt_path, default):
    with open(txt_path, 'r', encoding='utf-8') as file:
        # 0: power; 1: para; 2: \n
        line_cnt = 0
        for line in file.readlines():
            if "$end$" in line:
                break
            if line_cnt % 3 == 0:
                str_buf = ""
                cnt = 0
                for char in line:
                    if char.isdigit() or char ==".":
                        str_buf = str_buf + char
                    else:
                        if len(str_buf):
                            # print(float(str_buf))
                            if cnt < 5:
                                pkg.append(float(str_buf))
                            elif cnt < 10:
                                ram.append(float(str_buf))
                            elif cnt < 15:
                                tim.append(float(str_buf))
                            elif cnt < 20:
                                gpu.append(float(str_buf))
                            else:
                                pre.append(float(str_buf))
                            cnt += 1
                        str_buf = ""
            elif line_cnt % 3 == 1:
                par_name = line.split(" ")[0]
                if par_name == "p":
                    par_val = 0
                else:
                    par_buf = ""
                    for char in par_name:
                        if char.isdigit() or char == ".":
                            par_buf = par_buf + char
                    par_val = float(par_buf)
                for i in range(5):
                    par.append(par_val)
            else:
                # print(par)
                # print(pkg)
                # print(ram)
                # print(gpu)
                # print(tim)
                # print(pre)
                if line_cnt == 2:
                    par.clear()
                    par_val = default_epoch
                    for i in range(5):
                        par.append(par_val)
                    all_epoch["par"].extend(par)
                    all_epoch["pkg"].extend(pkg)
                    all_epoch["ram"].extend(ram)
                    all_epoch["gpu"].extend(gpu)
                    all_epoch["tim"].extend(tim)
                    all_epoch["pre"].extend(pre)
                    par.clear()
                    par_val = default_lr
                    for i in range(5):
                        par.append(par_val)
                    all_lr["par"].extend(par)
                    all_lr["pkg"].extend(pkg)
                    all_lr["ram"].extend(ram)
                    all_lr["gpu"].extend(gpu)
                    all_lr["tim"].extend(tim)
                    all_lr["pre"].extend(pre)
                    par.clear()
                    par_val = default
                    for i in range(5):
                        par.append(par_val)
                    if default == default_gamma:
                        all_gamma["par"].extend(par)
                        all_gamma["pkg"].extend(pkg)
                        all_gamma["ram"].extend(ram)
                        all_gamma["gpu"].extend(gpu)
                        all_gamma["tim"].extend(tim)
                        all_gamma["pre"].extend(pre)
                    elif default == default_wd:
                        all_wd["par"].extend(par)
                        all_wd["pkg"].extend(pkg)
                        all_wd["ram"].extend(ram)
                        all_wd["gpu"].extend(gpu)
                        all_wd["tim"].extend(tim)
                        all_wd["pre"].extend(pre)
                elif line_cnt < 18:
                    all_epoch["par"].extend(par)
                    all_epoch["pkg"].extend(pkg)
                    all_epoch["ram"].extend(ram)
                    all_epoch["gpu"].extend(gpu)
                    all_epoch["tim"].extend(tim)
                    all_epoch["pre"].extend(pre)
                elif line_cnt < 33:
                    all_lr["par"].extend(par)
                    all_lr["pkg"].extend(pkg)
                    all_lr["ram"].extend(ram)
                    all_lr["gpu"].extend(gpu)
                    all_lr["tim"].extend(tim)
                    all_lr["pre"].extend(pre)
                else:
                    if default == default_gamma:
                        all_gamma["par"].extend(par)
                        all_gamma["pkg"].extend(pkg)
                        all_gamma["ram"].extend(ram)
                        all_gamma["gpu"].extend(gpu)
                        all_gamma["tim"].extend(tim)
                        all_gamma["pre"].extend(pre)
                    elif default == default_wd:
                        all_wd["par"].extend(par)
                        all_wd["pkg"].extend(pkg)
                        all_wd["ram"].extend(ram)
                        all_wd["gpu"].extend(gpu)
                        all_wd["tim"].extend(tim)
                        all_wd["pre"].extend(pre)
                par.clear()
                pkg.clear()
                ram.clear()
                gpu.clear()
                tim.clear()
                pre.clear()
            line_cnt += 1


def display():
    print(all_epoch)
    print(all_lr)
    print(all_gamma)
    print(all_wd)


def plot_key(defualt):
    me_p = []
    me_p.append(pearson(all_epoch["par"], all_epoch["pkg"]))
    me_p.append(pearson(all_epoch["par"], all_epoch["ram"]))
    me_p.append(pearson(all_epoch["par"], all_epoch["gpu"]))
    me_p.append(pearson(all_epoch["par"], all_epoch["tim"]))
    me_p.append(pearson(all_epoch["par"], all_epoch["pre"]))
    sme_p = []
    sme_p.append(spearman(all_epoch["par"], all_epoch["pkg"]))
    sme_p.append(spearman(all_epoch["par"], all_epoch["ram"]))
    sme_p.append(spearman(all_epoch["par"], all_epoch["gpu"]))
    sme_p.append(spearman(all_epoch["par"], all_epoch["tim"]))
    sme_p.append(spearman(all_epoch["par"], all_epoch["pre"]))
    pme_p = []
    pme_p.append(p_pearson(all_epoch["par"], all_epoch["pkg"]))
    pme_p.append(p_pearson(all_epoch["par"], all_epoch["ram"]))
    pme_p.append(p_pearson(all_epoch["par"], all_epoch["gpu"]))
    pme_p.append(p_pearson(all_epoch["par"], all_epoch["tim"]))
    pme_p.append(p_pearson(all_epoch["par"], all_epoch["pre"]))
    spme_p = []
    spme_p.append(p_spearman(all_epoch["par"], all_epoch["pkg"]))
    spme_p.append(p_spearman(all_epoch["par"], all_epoch["ram"]))
    spme_p.append(p_spearman(all_epoch["par"], all_epoch["gpu"]))
    spme_p.append(p_spearman(all_epoch["par"], all_epoch["tim"]))
    spme_p.append(p_spearman(all_epoch["par"], all_epoch["pre"]))

    ml_p = []
    ml_p.append(pearson(all_lr["par"], all_lr["pkg"]))
    ml_p.append(pearson(all_lr["par"], all_lr["ram"]))
    ml_p.append(pearson(all_lr["par"], all_lr["gpu"]))
    ml_p.append(pearson(all_lr["par"], all_lr["tim"]))
    ml_p.append(pearson(all_lr["par"], all_lr["pre"]))
    sml_p = []
    sml_p.append(spearman(all_lr["par"], all_lr["pkg"]))
    sml_p.append(spearman(all_lr["par"], all_lr["ram"]))
    sml_p.append(spearman(all_lr["par"], all_lr["gpu"]))
    sml_p.append(spearman(all_lr["par"], all_lr["tim"]))
    sml_p.append(spearman(all_lr["par"], all_lr["pre"]))
    pml_p = []
    pml_p.append(p_pearson(all_lr["par"], all_lr["pkg"]))
    pml_p.append(p_pearson(all_lr["par"], all_lr["ram"]))
    pml_p.append(p_pearson(all_lr["par"], all_lr["gpu"]))
    pml_p.append(p_pearson(all_lr["par"], all_lr["tim"]))
    pml_p.append(p_pearson(all_lr["par"], all_lr["pre"]))
    spml_p = []
    spml_p.append(p_spearman(all_lr["par"], all_lr["pkg"]))
    spml_p.append(p_spearman(all_lr["par"], all_lr["ram"]))
    spml_p.append(p_spearman(all_lr["par"], all_lr["gpu"]))
    spml_p.append(p_spearman(all_lr["par"], all_lr["tim"]))
    spml_p.append(p_spearman(all_lr["par"], all_lr["pre"]))

    if defualt == default_gamma:
        mg = all_gamma["par"]
        mg_pkg = all_gamma["pkg"]
        mg_ram = all_gamma["ram"]
        mg_gpu = all_gamma["gpu"]
        mg_tim = all_gamma["tim"]
        mg_pre = all_gamma["pre"]
    elif defualt == default_wd:
        mg = all_wd["par"]
        mg_pkg = all_wd["pkg"]
        mg_ram = all_wd["ram"]
        mg_gpu = all_wd["gpu"]
        mg_tim = all_wd["tim"]
        mg_pre = all_wd["pre"]
    else:
        mg = []
        mg_pkg = []
        mg_ram = []
        mg_gpu = []
        mg_tim = []
        mg_pre = []
    mg_p = []
    mg_p.append(pearson(mg, mg_pkg))
    mg_p.append(pearson(mg, mg_ram))
    mg_p.append(pearson(mg, mg_gpu))
    mg_p.append(pearson(mg, mg_tim))
    mg_p.append(pearson(mg, mg_pre))
    smg_p = []
    smg_p.append(spearman(mg, mg_pkg))
    smg_p.append(spearman(mg, mg_ram))
    smg_p.append(spearman(mg, mg_gpu))
    smg_p.append(spearman(mg, mg_tim))
    smg_p.append(spearman(mg, mg_pre))
    pmg_p = []
    pmg_p.append(p_pearson(mg, mg_pkg))
    pmg_p.append(p_pearson(mg, mg_ram))
    pmg_p.append(p_pearson(mg, mg_gpu))
    pmg_p.append(p_pearson(mg, mg_tim))
    pmg_p.append(p_pearson(mg, mg_pre))
    spmg_p = []
    spmg_p.append(p_spearman(mg, mg_pkg))
    spmg_p.append(p_spearman(mg, mg_ram))
    spmg_p.append(p_spearman(mg, mg_gpu))
    spmg_p.append(p_spearman(mg, mg_tim))
    spmg_p.append(p_spearman(mg, mg_pre))

    data = np.array((me_p, ml_p, mg_p))
    # print(data)
    sdata = np.array((sme_p, sml_p, smg_p))
    # print(sdata)
    pdata = np.array((pme_p, pml_p, pmg_p))
    # print(pdata)
    spdata = np.array((spme_p, spml_p, spmg_p))

    return data, sdata, pdata, spdata


def single_plot(data, sdata, key, save_name):
    xl = ["pkg", "ram", "gpu", "tim", "pre"]
    yl = ["epochs", "lr", "gamma"]
    ylw = ["epochs", "lr", "weight decay"]
    ylt = ["epochs", "lr", "threshold"]

    if key == 0:
        matrix = data
        save_path = "fig/" + save_name + "_pearson.jpg"
    elif key == 1:
        matrix = sdata
        save_path = "fig/" + save_name + "_spearman.jpg"
    # else:
    #     hm = sb.heatmap(pdata, annot=True, xticklabels=xl,
    #                     yticklabels=yl)
    #     save_path = "fig/" + save_name + "_P_value.jpg"

    # mnist
    plt.subplot(2, 3, 1)
    hm = sb.heatmap(matrix, annot=True, xticklabels=xl,
                    yticklabels=yl)
    plt.title("mnist")

    # mnist
    plt.subplot(2, 3, 2)
    hm = sb.heatmap(matrix, annot=True, xticklabels=xl,
                    yticklabels=yl)
    plt.title("mnist")

    # mnist
    plt.subplot(2, 3, 3)
    hm = sb.heatmap(matrix, annot=True, xticklabels=xl,
                    yticklabels=yl)
    plt.title("mnist")

    # mnist
    plt.subplot(2, 3, 4)
    hm = sb.heatmap(matrix, annot=True, xticklabels=xl,
                    yticklabels=yl)
    plt.title("mnist")

    # mnist
    plt.subplot(2, 3, 5)
    hm = sb.heatmap(matrix, annot=True, xticklabels=xl,
                    yticklabels=yl)
    plt.title("mnist")

    plt.show()


def multi_plot(data, key, save_name):
    xl = ["pkg", "ram", "gpu", "tim", "pre"]
    yl = ["epochs", "lr", "gamma"]
    ylw = ["epochs", "lr", "weight decay"]
    ylt = ["epochs", "lr", "threshold"]

    matrix = data[key]
    if key == 0:
        t = "pearson"
    elif key == 1:
        t = "spearman"
    elif key == 2:
        t = "pearson p value"
    elif key == 3:
        t = "spearman p value"

    # mnist
    plt.subplot(2, 3, 1)
    hm = sb.heatmap(matrix[0], annot=True, xticklabels=xl,
                    yticklabels=yl)
    plt.title(save_name[0])

    # mff
    plt.subplot(2, 3, 2)
    hm = sb.heatmap(matrix[1], annot=True, xticklabels=xl,
                    yticklabels=ylt)
    plt.title(save_name[1])

    # siamese
    plt.subplot(2, 3, 3)
    hm = sb.heatmap(matrix[2], annot=True, xticklabels=xl,
                    yticklabels=yl)
    plt.title(save_name[2])

    # resnet
    plt.subplot(2, 3, 4)
    hm = sb.heatmap(matrix[3], annot=True, xticklabels=xl,
                    yticklabels=ylw)
    plt.title(save_name[3])

    # hr18
    plt.subplot(2, 3, 5)
    hm = sb.heatmap(matrix[4], annot=True, xticklabels=xl,
                    yticklabels=ylw)
    plt.title(save_name[4])

    plt.suptitle(t)
    plt.savefig("fig/" + t + ".jpg")
    plt.show()


def init(name):
    e = 0
    l = 0
    g = 0
    if name == "mff":
        e = 1000.0
        l = 0.03
        # threshold
        g = 2.0
    if name == "mnist_new" or name == "siamese_new":
        e = 14.0
        l = 1.0
        g = 0.7
    if name == "resnet":
        e = 200.0
        l = 0.2
        # weight decay
        g = 1e-4
    if name == "hr18":
        e = 60.0
        l = 0.05
        # weight decay
        g = 5e-4
    return e, l, g


def all_clear():
    all_epoch["par"].clear()
    all_epoch["pkg"].clear()
    all_epoch["ram"].clear()
    all_epoch["gpu"].clear()
    all_epoch["tim"].clear()
    all_epoch["pre"].clear()
    all_lr["par"].clear()
    all_lr["pkg"].clear()
    all_lr["ram"].clear()
    all_lr["gpu"].clear()
    all_lr["tim"].clear()
    all_lr["pre"].clear()
    all_gamma["par"].clear()
    all_gamma["pkg"].clear()
    all_gamma["ram"].clear()
    all_gamma["gpu"].clear()
    all_gamma["tim"].clear()
    all_gamma["pre"].clear()


# key = 0
# name = "mnist_new"
# path = name + ".txt"
#
# default_epoch, default_lr, default_gamma = init(name)
# default_wd = 0
#
# read(path, default_gamma)
# display()
# d, sd, p, sp = plot_key(default_gamma)
# single_plot(d, sd, key, name)

# 0: pearson
# 1: spearman
# 2: pearson p value
# 3: spearman p value
key = 1

paths = ["mnist_new", "mff", "sia", "resnet", "hr18"]
vec_d = []
vec_sd = []
vec_p = []
vec_sp = []
for i in range(5):
    # init
    name = paths[i]
    default_epoch, default_lr, default_gamma = init(name)
    default_wd = 0
    # read file
    read(name + ".txt", default_gamma)
    display()
    d, sd, p, sp = plot_key(default_gamma)
    vec_d.append(d)
    vec_sd.append(sd)
    vec_p.append(p)
    vec_sp.append(sp)
    all_clear()

vec = []
vec.append(vec_d)
vec.append(vec_sd)
vec.append(vec_p)
vec.append(vec_sp)

multi_plot(vec, key, paths)
