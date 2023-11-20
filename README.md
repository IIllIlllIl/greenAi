# greenAi
***
This is the mutation test framework to estimate how Deep Learning (DL) hyperparameters effect the energy consumption. It can mutate the hyperparameters and collect the energy metrics of package, RAM and GPU. Besides, it can analyze the correlation and trade-off between the metrics and hyperparameters. This framework is designed base on [ICSE_2022_artifact](https://github.com/stefanos1316/ICSE_2022_artifact). <br>
This repository contains:
- `mutation`: codes to conduct mutation tests on DL models. We done our mutation test on five open-source DL programs, including [mnist](https://github.com/pytorch/examples/tree/main/mnist), [mnist_forward_forward](https://github.com/pytorch/examples/tree/main/mnist_forward_forward), [siamese_network](https://github.com/pytorch/examples/tree/main/siamese_network), [pytorch_resnet_cifar10](https://github.com/akamaster/pytorch_resnet_cifar10), and [Person_reID_baseline_pytorch](https://github.com/layumi/Person_reID_baseline_pytorch). The codes are organized by the name of five models. Each directory inlcudes `governor.sh`, `run.sh`, `shell.py`, and`result`. <br>
- `mutation/*/governor.sh `: a shell code to switch the CPU setting. <br>
- `mutation/*/run.sh `: This is a script to start the training and collect the energy metrics. Therefore, it is writen base on the command line instructions to train the model. <br>
- `mutation/*/shell.py `: a python script to mutate the hyperparameters and call `run.sh` to train the mutation. It repeats the mutation test automatically and write the result into `result`. <br>
- `mutation/*/result `: the directory consists of `collect.py` and `data`. `collect.py` is a python script to collect the output of `shell.py` in`data` and process the original output and organize them. <br>
- `analysis`: data and codes to conduct the analysis. The data we collected are organized in `analysis/comp` and `analysis/*.txt`, which are collected form `mutation`. The three python scripts can conduct three types of analysis, including correlation analysis, trade-off analysis and parallel analysis. <br>

# Prerequisite
***
- Linux version 5.19.0-45-generic
- perf
- nvidia-smi
- Python 3.7.0

Be cautious that the fuction we used of perf may not work on some devices.

# Installation
***
1. Download this repository by: <br>
	git clone https://github.com/IIllIlllIl/greenAi.git
2. Install the tools (perf and nvidia-smi).
# Mutation
***

# Analysis
***

# Run on your own models
***
