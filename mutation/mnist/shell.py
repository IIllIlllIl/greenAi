import os
import subprocess
import argparse
import random
import math

# ser reputation
mutate_reputation = 5
cmd_reputation = 5


def modify_epoch(current_epoch, target=None):
    if target is None:
        flag = random.sample([-1, 1], 1)[0]
        if flag == 1:
            new_epoch = current_epoch - int(current_epoch * random.random() * 0.25)
        else:
            new_epoch = current_epoch + int(current_epoch * random.random() * 0.25)
        # make sure new_epoch != cur_epoch, except cur_epoch is minimized (1)
        if new_epoch == current_epoch:
            new_epoch = max(1, min(10, new_epoch) - 1)
    else:
        new_epoch = target
    return new_epoch


def modify_lr(current_lr, target=None):
    new_lr = current_lr
    if target is not None:
        new_lr = float(target)
    else:
        # direction decides on which direction the lr should be modified.
        # +1: larger than 1, smaller than 11
        # -1: smaller than 1e-10, larger than 1e-16
        # if the random lr == cur_lr, generate again. Upperbound = 10 times
        iter_cnt = 0
        while iter_cnt < 10:
            direction = random.sample([-1, 1], 1)[0]
            if direction == 1:
                new_lr = random.sample([float(n) for n in range(1, 11)], 1)[0]
            else:
                new_lr = float("1e-{}".format(random.sample([num for num in range(10, 16, 1)], 1)[0]))
            if new_lr != current_lr:
                break
            else:
                iter_cnt += 1
    return new_lr


def modify_learning_rate(current_lr, target=None):
    if target is None:
        flag = random.sample([-1, 1], 1)[0]
        if flag == 1:
            new_lr = current_lr * math.pow(10, random.random())
            # new_epoch = current_epoch - int(current_epoch * random.random() * 0.25)
        else:
            new_lr = current_lr * math.pow(10, - random.random())
            # new_epoch = current_epoch + int(current_epoch * random.random() * 0.25)
        # new_lr = current_lr * math.pow(10, - random.random() * 2)
    else:
        new_lr = target
    return new_lr


def modify_weight_decay(current_epoch, target=None):
    if target is None:
        flag = random.sample([-1, 1], 1)[0]
        if flag == 1:
            new_wd = (current_epoch / (1 + random.random() * 4))
        else:
            new_wd = current_epoch + (current_epoch * random.random() * 2)
        # make sure new_epoch != cur_epoch, except cur_epoch is minimized (1)
    else:
        new_wd = target
    return new_wd


def modify_gamma(current_g, target=None):
    if target is None:
        flag = random.sample([-1, 1], 1)[0]
        if flag == 1:
            new_g = (current_g / (1 + random.random() * 4))
        else:
            new_g = current_g + (current_g * random.random() * 2)
        # make sure new_epoch != cur_epoch, except cur_epoch is minimized (1)
    else:
        new_g = target
    return new_g


def shell_cmd(cmd, file_name, max_count=24, tm=3600):
    # write log into "cmdLog" file
    log = open("./cmd_log", 'a')
    log.writelines(cmd + ": \n")
    log.close()

    i = 0
    cnt = 0
    # try to repeat
    while i < cmd_reputation and cnt < max_count:
        si = str(i)
        flag = False
        log = open("./cmd_log", 'a')
        os.system("rm *.log")
        # !!! save_resnet20
        # os.system("rm save_resnet20/*")
        try:
            p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, encoding="utf-8", timeout=tm)
            flag = True
        finally:
            if flag:
                if p.returncode == 0:
                    success = "success " + si + ":" + str(p)
                    print(success)
                    log.writelines(success + "\n")
                    file = file_name + "-" + si

                    # collect data
                    os.mkdir(file)
                    os.system("mv *.log ./" + file)
                    # !!! save_resnet20
                    # os.system("mv save_resnet20/* ./" + file)
                    os.system("mv " + file + " ./result")
                    i += 1
                else:
                    error = "error " + si + ":" + str(p)
                    print(error)
                    log.writelines(error + "\n")
            else:
                # record failure and continue
                error = "error " + si + ": is not finish"
                print(error)
                log.writelines(error + "\n")
            log.close()
            cnt += 1
            continue

    log.close()


def shell(key, target, tm=7200):
    cmd = "bash run.sh -" + key + " " + str(target)
    result_file = "p" + key + str(target)
    # print(cmd + " " + result_file)
    shell_cmd(cmd, result_file, tm)


def mutate(key, current_target, mutate_target=None):
    # epoch
    if key == "epochs":
        print("modify epoch")
        buf = []
        for mi in range(mutate_reputation):
            epoch = modify_epoch(current_target, mutate_target)
            while epoch in buf:
                epoch = modify_epoch(current_target, mutate_target)
            buf.append(epoch)
            shell("e", epoch)
    elif key == "lr":
        print("modify learning rate")
        for mi in range(mutate_reputation):
            lr = modify_learning_rate(current_target, mutate_target)
            shell("l", lr)
    elif key == "g":
        print("modify gamma")
        for mi in range(mutate_reputation):
            g = modify_gamma(current_target, mutate_target)
            shell("g", g)


parser = argparse.ArgumentParser()
parser.add_argument('-k', '--key', default="NA", type=str)
parser.add_argument('-e', '--epochs', default=14, type=int)
parser.add_argument('-l', '--learning-rate', default=1.0, type=float)
parser.add_argument('-g', '--gamma', default=0.7, type=float)
parser.add_argument('-mr', '--mutate-reputation', default=mutate_reputation, type=int)
parser.add_argument('-cr', '--cmd-reputation', default=cmd_reputation, type=int)
args = parser.parse_args()

mutate_key = args.key
mutate_reputation = args.mutate_reputation
cmd_reputation = args.cmd_reputation
os.system("rm cmd_log")

if mutate_key == "all":
    shell("e", args.epochs)
    mutate("lr", args.learning_rate)
    mutate("g", args.gamma)
    mutate("epochs", args.epochs)
elif mutate_key == "epochs":
    print(args.epochs)
    mutate(mutate_key, args.epochs)
elif mutate_key == "lr":
    print(args.learning_rate)
    mutate(mutate_key, args.learning_rate)
elif mutate_key == "g":
    print(args.gamma)
    mutate(mutate_key, args.gamma)
elif mutate_key == "measure":
    test = [14]
    mutate_reputation = 5
    for i in range(len(test)):
        shell("e", test[i])

