# greenAi
***
This is the mutation test framework to estimate how Deep Learning (DL) hyperparameters effect the energy consumption. It can mutate the hyperparameters and collect the energy metrics of package, RAM and GPU. Besides, it can analyze the correlation and trade-off between the metrics and hyperparameters. This framework is designed base on [ICSE_2022_artifact](https://github.com/stefanos1316/ICSE_2022_artifact). <br>
This repository contains:
- `mutation`: codes to conduct mutation tests on DL models. We done our mutation test on five open-source DL programs, including [mnist](https://github.com/pytorch/examples/tree/main/mnist), [mnist_forward_forward](https://github.com/pytorch/examples/tree/main/mnist_forward_forward), [siamese_network](https://github.com/pytorch/examples/tree/main/siamese_network), [pytorch_resnet_cifar10](https://github.com/akamaster/pytorch_resnet_cifar10), and [Person_reID_baseline_pytorch](https://github.com/layumi/Person_reID_baseline_pytorch). The codes are organized by the name of five models. Each directory inlcudes `governor.sh`, `run.sh`, `shell.py`, and`result`. <br>
- `mutation/*/governor.sh `: a shell code to switch the CPU setting. <br>
- `mutation/*/run.sh `: This is a script to start the training and collect the energy metrics. Therefore, it is writen base on the command line instructions to train the model. <br>
- `mutation/*/shell.py `: a python script to mutate the hyperparameters and call `run.sh` to train the mutation. It repeats the mutation test automatically and write the result into `result`. <br>
- `mutation/*/result `: the directory consists of `collect.py` and `data`. `collect.py` is a python script to collect the output of `shell.py` in`data` and process the original output and organize them. <br>
- `analysis`: data and codes to conduct the analysis. The data we collected are organized in `analysis/comp/*.txt` and `analysis/*.txt`, which are collected form `mutation`. The three python scripts can conduct three types of analysis, including correlation analysis, trade-off analysis and parallel analysis. <br>

# Prerequisite
***
- Linux version 5.19.0-45-generic
- perf
- nvidia-smi
- Python 3.7.0

# Installation
***
1. Download this repository by:

		git clone https://github.com/IIllIlllIl/greenAi.git

2. Install the tools (`perf` and `nvidia-smi`). The vision of tools are depends on your own operationg system. Be cautious that the fuction we used of `perf` may not work on some devices.
3. Install the models and their datasets. They can be installed from their repositories.
	- [mnist](https://github.com/pytorch/examples/tree/main/mnist)
	- [mnist_forward_forward](https://github.com/pytorch/examples/tree/main/mnist_forward_forward)
	- [siamese_network](https://github.com/pytorch/examples/tree/main/siamese_network)
	- [pytorch_resnet_cifar10](https://github.com/akamaster/pytorch_resnet_cifar10)
	- [Person_reID_baseline_pytorch](https://github.com/layumi/Person_reID_baseline_pytorch)
4. Install the relative Python codebase by:

		pip install -r requirements.txt

# Mutation
***
1. To run our mutation test on the five models, we need to copy our files to its repository downloaded from GIthub. For a chosen model, the needed files inclues `governor.sh`, `run.sh`, `shell.py`, and`result` under the directory with the name of the model in 'mutation'. The files above should be copied to the same directory with the tarining code, such as `main.py` or `train.py`.
2. Then we can use 'shell.py' to run our experiment, like

		python shell.py -k measure

	This commad will mutate all hyperparameters and collects the metrics. `-k` defines the  type of mutation. if you wish to mutate a single hyperparameter, like change `epochs` to value 0.1, you can use the option, like

		python shell.py -k epochs -e 0.1

	The options we provide can be list by:

		python shell.py -h

3. The reuslts of the `shell.py` will be written to the 'result' directory. We can check them there. The files of the result will be named like `pe190-0`. `e` means this mutation has different `epochs` value, 190. `-0` means this is the first repeat of this mutation.

# Analysis
***
1. To analyze the metrics, we need to reorganize the output of the mutation first. Or you can use the data we prepared in `analysis`. We can use `collect.py` to do all this work under the `result` directory. First, we reorganize the output and write them into the `data` directory. For example, if we wants to collect the data `pe190`, which includes `pe190-0`, `pe190-1`, `pe190-2`, `pe190-3`, and `pe190-4`, we can use the command:

		python collect.py -c pe190

	Be cautious that the output of original model is also named as `pe200` (here we assume the original value of `epochs` is 200). To collect these data, we should rename them before run `collect.py` by

		cp pe200-0 p-0

2. After reorganization, execute `collect.py ` again to compile the results:

		python collect.py -n pe190

	The output of this command should be copied into a text file like `analysis/*.txt` we provided. Then move these text file to the `analysis` directory.

3. With these text files, we can run the analysis codes, make sure that you replace the text file we provide with same file name. Run the corresponding python code to run the analysis. For instance, to run the correlation analysis, 

		python rq1-correlation.py

	`rq1-correlation.py` conducts the correlation analysis between hyperparameters and metrics. `rq2-trade-off.py` conducts the trade-off analysis in common environments and parallel environments. `rq3-parallel.py` conducts the correlation analysis in parallel environments.

# Run on your own models
***
To run the code on your own models, three scripts in `mutation` should be modified, including `run.sh`, `shell.py`, and`collect.py`. 
- `run.sh`:
- `shell.py`: 
- `collect.py `: 

Also, the codes in `analysis` need to be modified. The 